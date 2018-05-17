import bt
from bt.core import Algo, AlgoStack
from future.utils import iteritems
import pandas as pd
import numpy as np
import pdb

class RunOnDate(Algo):
    
    def __init__(self, dates):
        super(RunOnDate, self).__init__()
        self.dates =dates

    def __call__(self, target):
        return target.now in self.dates


class RunSigHappens(Algo): 
    
    """
    只在信号signal为True的时候return True。本身跟RunOnDate差不多

    Args:
        * signal(Series): index为日期的Series，values为True和False

    """

    def __init__(self, signal, include_no_data=False):
        super(RunSigHappens, self).__init__()
        self.signal = signal
        self.include_no_data = include_no_data
    
    def __call__(self, target):
        if target.now in self.signal.index:
            sig = self.signal.loc[target.now]
            if sig.values:
                return True

        return False



class MaintainCash(Algo):

    """
    下次rebalance前维持的现金量，通常会接上Rebalance算法

    Args:
        * cash(double):设置为0到1之间的数字，表示保留多少作为现金

    Sets:
        * cash

    """
    def __init__(self,cash=0):
        super(MaintainCash, self).__init__()
        self.cash=cash
    
    def __call__(self,target):
        target.temp['cash']=self.cash
        return True



class SetTemp(Algo):
    """
    该算法输入一个Series，并事先指定一个字段temp_key，运行时如果Series中包含当前时刻，
    那么就会把temp中的temp_key字段设置为对应data；如果不包含当前时刻(Target.now)，返回False。

    Args:
        * data(Series)：index为日期的值序列
        * temp_key(str)：在temp中设置的字段名字

    """
    def __init__(self,data,temp_key,dropna=True,empty_allowed=False):
        super(SetTemp, self).__init__()
        self.data=data
        self.temp_key=temp_key
        self.dropna=dropna
        self.empty_allowed=empty_allowed
        
    def __call__(self,target):
        #pdb.set_trace()
        if (self.data is None) or (target.now not in self.data.index):
            if self.empty_allowed:
                target.temp[self.temp_key]=pd.Series()
            else:
                pass
            return True
        
        #print(target.now)
        if target.now in self.data.index:
            if self.dropna:
                target.temp[self.temp_key] = self.data.loc[target.now].dropna() 
            else:
                target.temp[self.temp_key] = self.data.loc[target.now]

        return True


class SelectOnSelect(Algo):
    """
    基于已有select，然后再额外添加条件，只能是交集、或者是差集。

    Args:
        * signal(DataFrame): index为日期，columns为universe空间。值为True或者False

    Sets:
        * selected

    Requires:
        * selected
    """

    def __init__(self, signal, include_no_data=False):
        super(SelectOnSelect, self).__init__()
        self.signal = signal
        self.include_no_data = include_no_data

    def __call__(self,target):
        if target.now in self.signal.index:
            sig = self.signal.loc[target.now]
            # get tickers where True
            selected = list(sig[sig].index)
            
            if 'selected' not in target.temp:
                target.temp['selected'] = list(selected)
            else:
                selected_set=set(target.temp['selected']).intersection(set(selected))
                target.temp['selected']=list(selected_set)

        return True
        


class RebalanceByPosition(Algo):
    def __init__(self,price):
        super(RebalanceByPosition, self).__init__()
        self.price=price
    
    def __call__(self, target):
        if 'positions' not in target.temp:
            return True
        
        targets = target.temp['positions']
        
        #pdb.set_trace()
        # de-allocate children that are not in targets and have non-zero value
        # (open positions)
        for cname in target.children:
            # if this child is in our targets, we don't want to close it out
            if cname in targets:
                continue

            # get child and value
            c = target.children[cname]
            v = c.value
            # if non-zero and non-null, we need to close it out
            if v != 0. and not np.isnan(v):
                target.close(cname)
        
        base=target.value

        nowprice=self.price.loc[target.now,:]

        for item in iteritems(targets):
            iweight=item[1]*nowprice[item[0]]/base
            target.rebalance(iweight, child=item[0], base=base)

        return True
#%%
class DeltaBuySellWeight(Algo):
    
    def __init__(self,buy_allowed,sell_allowed):
        super(DeltaBuySellWeight, self).__init__()
        self.buy_allowed=buy_allowed
        self.sell_allowed=sell_allowed
        
    def __call__(self,target):
        # 1.如果不含有未平衡的项目
        if 'remainweights' not in self.perm:
            return True
        
        # 2.如果未平衡的项目为空
        if len(self.perm['remainweights'])==0:
            return True
        
        # 3.读取可以买卖的清单
        b_allowed_i=self.buy_allowed.iloc[target.now,:]
        s_allowed_i=self.sell_allowed.iloc[target.now,:]
        
        # 4. 计算base
        # save value because it will change after each call to allocate
        # use it as base in rebalance calls
        base = target.value

        # If cash is set (it should be a value between 0-1 representing the
        # proportion of cash to keep), calculate the new 'base'
        if 'cash' in target.temp:
            base = base * (1 - target.temp['cash'])
            
        # 5. 初始化可以交易的名单
        poplist=[]
        
        # 6. 循环处理       
        for item in iteritems(self.perm['remainweights']):
            # 如果要买且可以买
            if (item[1]>0) & b_allowed_i[item[0]]:
                target.allocate(item[1]*base,child=item[0])
                poplist.append(item[0])
            # 如果要卖且可以卖    
            elif (item[1]<0) & s_allowed_i[item[0]]:
                target.allocate(item[1]*base,child=item[0])
                poplist.append(item[0])
                
        # 7.去除已经交易掉的项目
        for popi in poplist:
            self.perm['remainweights'].pop(popi)
            
        return True
        
#%% 
class OptWeights(Algo):
    def __init__(self,optimizer,alpha_return,bench_weights,style_factor):
        super(OptWeights, self).__init__()
        self.optimizer=optimizer
        self.alpha_return=alpha_return
        self.bench_weights=bench_weights
        self.style_factor=style_factor
        
    def __call__(self,target):
        self.optimizer.alpha_return=self.alpha_return.loc[target.now,:]
        if self.bench_weights is not None:
            self.optimizer.bench_weights=self.bench_weights.loc[target.now,:]
        if self.style_factor is not None:
            sf_now={}
            #pdb.set_trace()
            for istyle in self.style_factor:
                sf_now[istyle]=self.style_factor[istyle].loc[target.now,:]
            self.optimizer.style_factor=pd.DataFrame(sf_now)
            
        self.optimizer.port_weights()
        weights=self.optimizer.weights_opt.dropna()
        #pdb.set_trace()
        target.temp['weights']=weights[(weights>=0.001)|(weights<-0.001)].to_dict()
        
        return True

#%%
class DealClose(Algo):
    """
    处理残留的remained_toclose
    Requires:
        * remained_toclose(perm): 需要平仓但却尚未平掉的
        * buy_not_allowed: 
        * sell_not_allowed:
    """
    def __init__(self):
        super(DealClose, self).__init__()
        
    def __call__(self, target):
        if 'remained_toclose' not in target.perm:
            return True
        
        if len(target.perm['remained_toclose'])==0:
            return True
        
        #pdb.set_trace()
        targets=target.perm['remained_toclose']
        
        if 'buy_not_allowed' in target.temp:
            buy_not_allowed=target.temp['buy_not_allowed']
        else:
            buy_not_allowed=None
            
        if 'sell_not_allowed' in target.temp:
            sell_not_allowed=target.temp['sell_not_allowed']
        else:
            sell_not_allowed=None
        
        for cname in targets:
            if cname not in target.children: # 已经被平仓了
                targets.remove(cname)
                continue
            # 以下为对于要平仓的security
            # get child and value
            c = target.children[cname]
            w = c.weight
            
            if (sell_not_allowed is not None) and (w>0) and sell_not_allowed[cname]:# 需要卖却卖不了
                continue
                        
            if (buy_not_allowed is not None) and (w<0) and buy_not_allowed[cname]: # 需要买却买不了
                continue
            
            v = c.value
            # if non-zero and non-null, we need to close it out
            if v != 0. and not np.isnan(v):
                target.close(cname)
                targets.remove(cname)
        
        #target.perm['remained_toclose']=targets
        
        return True
        
#%% 
class RebalanceBuySellAllowed(Algo):

    """
    比原本的Rebalance考虑了能否买卖的问题

    Requires:
        * buy_not_allowed
        * sell_not_allowed
        * weights
        * cash (optional): You can set a 'cash' value on temp. This should be a
            number between 0-1 and determines the amount of cash to set aside.
            For example, if cash=0.3, the strategy will allocate 70% of its
            value to the provided weights, and the remaining 30% will be kept
            in cash. If this value is not provided (default), the full value
            of the strategy is allocated to securities.
    
    Args:
        * remained_toclose: 那些需要平仓但是没有平掉的，放在下次
    """

    def __init__(self):
        super(RebalanceBuySellAllowed, self).__init__()
        
    def __call__(self, target):
        if 'weights' not in target.temp:
            return True

        targets = target.temp['weights']

        # de-allocate children that are not in targets and have non-zero value
        # (open positions)
        
        if 'buy_not_allowed' in target.temp:
            buy_not_allowed=target.temp['buy_not_allowed']
        else:
            buy_not_allowed=None
            
        if 'sell_not_allowed' in target.temp:
            sell_not_allowed=target.temp['sell_not_allowed']
        else:
            sell_not_allowed=None
            
        remained_toclose=[]
        
        for cname in target.children:
            # if this child is in our targets, we don't want to close it out
            if cname in targets:
                continue
            
            # 以下为对于要平仓的security
            # get child and value
            c = target.children[cname]
            w = c.weight
            
            if (sell_not_allowed is not None) and (w>0) and sell_not_allowed[cname]:
                remained_toclose.append(cname)
                continue
                        
            if (buy_not_allowed is not None) and (w<0) and buy_not_allowed[cname]:
                remained_toclose.append(cname)
                continue
            
            v = c.value
            # if non-zero and non-null, we need to close it out
            if v != 0. and not np.isnan(v):
                target.close(cname)
        
        
        target.perm['remained_toclose']=remained_toclose
        # save value because it will change after each call to allocate
        # use it as base in rebalance calls
        base = target.value

        # If cash is set (it should be a value between 0-1 representing the
        # proportion of cash to keep), calculate the new 'base'
        if 'cash' in target.temp:
            base = base * (1 - target.temp['cash'])
        
        #pdb.set_trace()
        for item in iteritems(targets):
            w=item[1]
            cname=item[0]
            #pdb.set_trace()
            if (buy_not_allowed is not None) and (w>0) and buy_not_allowed[cname]:
                pass
            elif (sell_not_allowed is not None) and (w<0) and sell_not_allowed[cname]:
                pass
            else:
                target.rebalance(item[1], child=item[0], base=base)
        
        
        return True     
    

            
        