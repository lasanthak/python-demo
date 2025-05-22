import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

_diamonds = sns.load_dataset("diamonds")


def draw_scatter_plot1(diamonds):
    sns.set_theme(style="whitegrid")

    f, ax = plt.subplots(figsize=(10, 10))
    sns.despine(f, left=True, bottom=True)
    clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    sns.scatterplot(x="carat", y="price",
                    hue="clarity", size="depth",
                    palette="ch:r=-.2,d=.3_r",
                    hue_order=clarity_ranking,
                    sizes=(1, 10), linewidth=0,
                    data=diamonds, ax=ax)
    plt.show()


def draw_carat_price(df, ax, c):
    _x_values = df['carat']
    _y_values = df['price']
    ax.plot(_x_values, _y_values, c=c, marker='.', lw=0)


def reg_linear(df, ax, c):
    _x_values = df['carat']
    _y_values = df['price']
    _slope, _intercept, _r, _p, _std_err = stats.linregress(_x_values, _y_values)
    _y_pred = _slope * _x_values + _intercept
    # ax.plot(_x_values, _y_pred, c='#222222', lw=1)
    ax.plot(_x_values, _y_pred, c=c, lw=1)
    print(f'x,y : error={_std_err}, r={_r}, p={_p}')


def reg_linear_sqr(df, ax, c):
    _x_values = df['carat']
    _x2_values = _x_values * _x_values
    _y_values = df['price']
    _slope, _intercept, _r, _p, _std_err = stats.linregress(_x2_values, _y_values)
    _y_pred = _slope * _x2_values + _intercept
    ax.plot(_x_values, _y_pred, c='#222222', marker='.', lw=0)
    print(f'x:sqr(x): error={_std_err}, r={_r}, p={_p}')

def reg_linear_cube(df, ax, c):
    _x_values = df['carat']
    _x3_values = _x_values * _x_values * _x_values
    _y_values = df['price']
    _slope, _intercept, _r, _p, _std_err = stats.linregress(_x3_values, _y_values)
    _y_pred = _slope * _x3_values + _intercept
    ax.plot(_x_values, _y_pred, c='#222222', marker='.', lw=0)
    print(f'x:cube(x): error={_std_err}, r={_r}, p={_p}')



if __name__ == '__main__':
    _fig, _ax = plt.subplots(figsize=(10, 10))
    _fig.tight_layout(pad=3.0)
    # _ax.set_xlim([0, _diamonds['carat'].max()])
    _ax.set_xlim([0, 10])
    # _ax.set_ylim([0, _diamonds['price'].max()])
    _ax.set_ylim([0, 30000])

    _grouped = _diamonds.groupby('clarity')

    print(f'Diamonds ==> size:{_diamonds.size}')
    _colors = {"I1": "#ffafcc", "SI2": "#2a9d8f", "SI1": "#fb5607", "VS2": "#9b5de5",
               "VS1": "#606c38", "VVS2": "#9a8c98", "VVS1": "#d90429", "IF": "#03045e"}

    for _key, _gd in _grouped:
        #draw_carat_price(_gd, _ax, '#38b000')
        draw_carat_price(_gd, _ax, _colors[_key])

    for _key, _gd in _grouped:
        print('-----------------------------------------')
        print(f'Group: {_key}, Size: {_gd.size}')
        _c = _colors[_key]
        # reg_linear(_gd, _ax, _c)
        # reg_linear_sqr(_gd, _ax, _c)
        reg_linear_cube(_gd, _ax, _c)
    plt.show()
    print("Done")
