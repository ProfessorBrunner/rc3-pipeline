import  matplotlib.pyplot as plt
import numpy as np
def fit_and_plot(x,y,xlabel="",ylabel="",title="",zeroed=False,annotate_fit= True,right_words = False,error_bar="",sci_lim = False,annotate="",right_annotate=False,marker='o'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x,y,'{}'.format(marker))
    z = np.polyfit(x,y, 1) 
    print z
    p = np.poly1d(z)
    print p
    if zeroed : 
        a = np.linspace(0,max(x))
    else:
        a = np.linspace(min(x),max(x))
    ax1.plot(a, p(np.linspace(min(x),max(x))),color="red")
    if annotate_fit: 
        slope = z[0]
        intercept = z[1]
        if right_words:    
            ax1.text(0.48,0.85,"y= %.5f x + %.5f"%(slope,intercept), fontsize=13,transform=ax1.transAxes)
        else:
            ax1.text(0.03,0.85,"y= %.5f x + %.5f"%(slope,intercept), fontsize=13,transform=ax1.transAxes)
    if title !="":
        plt.title(title,fontsize=13 )    
        plt.xlabel(xlabel,fontsize=12)
        plt.ylabel(ylabel,fontsize=12)
#     ax1 = fig.add_subplot(111)
#     ax1.text(0.03,0.8,"y= %.5f x %.5f"%(p[0],p[1]), fontsize=13,transform=ax.transAxes)
    if annotate!="":
        if right_annotate: 
            ax1.text(0.48,0.85,annotate, fontsize=13,transform=ax1.transAxes)
    if error_bar!="":
        ax1.errorbar(x, y, yerr=error_bar, fmt='o')
    if sci_lim:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tick_params(axis='both', which='minor', labelsize=12)
    return p
    
#Code from Eduardo Martin (http://balbuceosastropy.blogspot.com/2013/09/the-mollweide-projection.html)
def plot_mwd(RA,Dec,org=0,title='Mollweide projection', projection='mollweide'):
    ''' RA, Dec are arrays of the same length.
    RA takes values in [0,360), Dec in [-90,90],
    which represent angles in degrees.
    org is the origin of the plot, 0 or a multiple of 30 degrees in [0,360).
    title is the title of the figure.
    projection is the kind of projection: 'mollweide', 'aitoff', 'hammer', 'lambert'
    '''
    x = np.remainder(RA+360-org,360) # shift RA values
    ind = x>180
    x[ind] -=360    # scale conversion to [-180, 180]
    x=-x    # reverse the scale: East to the left
    tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = np.remainder(tick_labels+360+org,360)
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection=projection, axisbg ='LightCyan')
    ax.scatter(np.radians(x),np.radians(Dec),marker='.',color='blue')  # convert degrees to radians
    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    ax.set_title(title)
    ax.title.set_fontsize(15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(12)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(12)
    ax.grid(True)