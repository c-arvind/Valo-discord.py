from matplotlib import pyplot as plt
import numpy as np

def plot(ratings):
    maxi=max(ratings)
    mini=min(ratings)
    plt.clf()
    fig, ax = plt.subplots(figsize =(12,5),dpi=200)
    colors = ["red" if i<0 else "green" for i in ratings]
    ax.bar(np.arange(0,len(ratings)/2,0.5),ratings, color=colors,zorder=2,width=0.35)

    
    # Remove axes splines
    for s in ['top', 'bottom', 'right']:
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color('white')
    plt.axhline(y=0, color='white', linestyle='-')
    ax.tick_params(colors='white')
    ax.axes.xaxis.set_visible(False)

    plt.yticks(range(mini-5,maxi+7,5))

    # Add x, y gridlines
    ax.grid(b = True, color ='white',

            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2,zorder=0)


    for i in ax.patches:
        #print(i)
        if i.get_height()>0:
            plt.text(i.get_x()+0.1, i.get_height()+1, '+' + str(round(i.get_height())),
                fontsize = 15, fontweight ='bold',
                color ='green')
        else:
            plt.text(i.get_x()+0.15, i.get_height()-2.5, str(round(i.get_height())),
                fontsize = 15, fontweight ='bold',
                color ='red')
        
        
    # Show Plot
    plt.savefig('saved_figure.png',transparent=True)
    plt.close()