import statsmodels.formula.api as smf

def regression(df,dep,indep):
    regg = smf.ols(formula=f"{dep} ~ {' + '.join(indep)}", data=df).fit()
    print(regg.summary())

def distributionBasedOnVix(df,col):
    for val in range(1,6):
        ultra_filtered = df[(df[col]!=0) & (df['V_coded']==val)]
        slightly_filtered = df[df['V_coded']==val]
        l1 = len(ultra_filtered)
        l2 = len(slightly_filtered)
        print(l1,l2)
        print(l1/l2)

def extremeCloseContinuation(df,rvol,direction):
    if direction.lower() == 'fade':
        multiplier = -1
    elif direction.lower() == 'hold':
        multiplier = 1
    fade_and_extreme = df[(df['ExCl']==multiplier*(df['Gap']/abs(df['Gap']))) & (df['Rvol']>rvol)]
    fade_and_extreme_continuation = df[(df['ExCl']==multiplier*(df['Gap']/abs(df['Gap']))) & (df['D2']==1) & (df['Rvol']>rvol)]
    print(len(fade_and_extreme_continuation),len(fade_and_extreme))
    print(f'{len(fade_and_extreme_continuation)/len(fade_and_extreme)*100:.2f}%')

def gapDownCloseUp(df):
    # df_gap = df[(df['Gap']<0) & (df['Low']<df['MA50']) & (df['Close']>df['YCl'])]
    df_gap = df[(df['Open']>df['MA50']) & (df['Low']<df['MA50']) & (df['Close']>df['Open'])]
    engulf = df_gap[df_gap['D2']==1]
    print(len(df_gap))
    print(len(engulf))
    print(len(engulf)/len(df_gap))

def filterConsecutiveRedDays(df):
    for i in range(1,5):
        df[f'yd{i}'] = df['Close'].shift(i)
    df = df[(df['yd1']<df['yd2'])&(df['yd2']<df['yd3'])&(df['yd3']<df['yd4'])]
    return df

def gapUpAfterRedDays(df):
    df=filterConsecutiveRedDays(df)
    gap_up = df[df['Open']>df['yd1']]
    gap_held = gap_up[(gap_up['Close']>gap_up['Open'])&(gap_up['ExCl']==1)]
    # gap_held = gap_up[(gap_up['Close']>gap_up['Open'])]
    df = df.drop(['yd1','yd2','yd3','yd4'],axis=1)
    print(len(gap_up))
    print(len(gap_held))
    print(len(gap_held)/len(gap_up))

def greenDayAfterRedDays(df):
    df=filterConsecutiveRedDays(df)
    green_day = df[df['Close']>df['yd1']]
    gap_held = green_day[green_day['Close']>green_day['Open']]
    df = df.drop(['yd1','yd2','yd3','yd4'],axis=1)
    print(len(green_day))
    print(len(gap_held))
    print(len(gap_held)/len(green_day))

def breakFakeAtMa(df):
    pass