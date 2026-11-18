"""Regenerate five Part I textbook figures with readable typography.
Synthetic numerical examples; not field measurements. Figure 5.2 is unchanged.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm

BLUE="#003262"; GOLD="#B17A00"; TEAL="#247C86"; RED="#AD3535"; GRAY="#8C9AAA"; INK="#20344A"

def root_dir(root=None):
    if root is not None: return Path(root)
    p=Path.cwd()
    return p.parent if p.name=="notebooks" else p

def style():
    plt.rcParams.update({"font.family":"serif","font.size":13.2,
      "axes.labelsize":14.5,"xtick.labelsize":12,"ytick.labelsize":12,
      "legend.fontsize":12,"axes.spines.top":False,"axes.spines.right":False,
      "pdf.fonttype":42,"ps.fonttype":42,"lines.linewidth":2.4,
      "axes.edgecolor":INK,"text.color":INK,"axes.labelcolor":INK})

def save(fig,stem,root):
    out=root_dir(root)/"figures";out.mkdir(parents=True,exist_ok=True)
    for name in (stem,):
        fig.savefig(out/(name+".pdf"),bbox_inches="tight",metadata={"CreationDate":None,"ModDate":None})
        fig.savefig(out/(name+".png"),dpi=180,bbox_inches="tight")
    plt.close(fig)
    return out/(stem+".pdf")

def bayes_theorem(root=None):
    style()
    prior=np.full(3,1/3);like=np.array([.8,.4,.1]);post=prior*like/(prior@like)
    assert np.allclose(post,[8/13,4/13,1/13])
    fig,axs=plt.subplots(1,3,figsize=(8.4,3.4),sharey=False)
    for j,(ax,vals,title) in enumerate(zip(axs,[prior,like,post],
                         ["PRIOR","MEASUREMENT LIKELIHOOD","POSTERIOR"])):
        yy=np.arange(3)
        ax.barh(yy,vals,height=.52,color=([GRAY]*3 if j==0 else [TEAL]*3 if j==1 else [BLUE]*3))
        for k,v in enumerate(vals):
            ax.text(v+.026,k,f"{v:.3f}",va="center",fontsize=12.5,weight="bold")
        ax.set_xlim(0,1.04);ax.set_ylim(2.6,-.6)
        ax.set_title(title,fontsize=12.7,weight="bold",pad=15)
        ax.set_yticks(yy,[r"$L_1$",r"$L_2$",r"$L_3$"] if j==0 else [""]*3)
        ax.tick_params(axis="y",length=0,pad=10,labelsize=17 if j==0 else 12)
        ax.set_xticks([0,.5,1]);ax.grid(axis="x",alpha=.13);ax.set_axisbelow(True)
        if j<2: ax.text(1.11,1,"→",transform=ax.transAxes,fontsize=21,weight="bold",
                        ha="center",va="center",color=GOLD)
        ax.set_xlabel(r"$P(D\mid L_i)$" if j==1 else "Probability")
    axs[2].text(.07,-.44,"Most probable",color=BLUE,fontsize=10.5,weight="bold",ha="left",va="center")
    fig.subplots_adjust(left=.065,right=.99,top=.85,bottom=.22,wspace=.36)
    return save(fig,"JNB2-bayes-theorem",root)


def updating_integrated(root=None):
    """Single Chapter 3 visualization with a four-element legend.

    The cyan-filled patch indicates an alternative second report, not
    a confidence or credible interval. All probabilities are synthetic.
    """
    style()
    from matplotlib.patches import Patch
    def update(p, positive, fpr=.20):
        a=.90 if positive else .10
        b=fpr if positive else 1-fpr
        return a*p/(a*p+b*(1-p))
    def history(fpr):
        vals=[.60]
        for _ in range(5):
            vals.append(update(vals[-1], True, fpr))
        return np.array(vals)
    correct=history(.20)
    optimistic=history(.05)
    negative_second=update(correct[1], False, .20)
    assert np.isclose(correct[2], .486/(.486+.016))
    assert np.isclose(negative_second, .054/(.054+.064))
    fig, ax=plt.subplots(figsize=(9.2,4.95))
    band_color="#B5C9DD"
    ax.axvspan(1.77,2.23,color=band_color,alpha=.76,zorder=0)
    h1=ax.plot(range(6),correct,color=BLUE,lw=3.0,marker="o",ms=8.6,
        label="Specified model · positive reports",zorder=3)[0]
    h2=ax.plot(range(6),optimistic,color=GOLD,lw=2.7,ls="--",marker="s",ms=8.1,
        label="Optimistic model · positive reports",zorder=3)[0]
    h3=ax.plot([1,2],[correct[1],negative_second],color=TEAL,lw=2.8,
        ls=":",marker="D",ms=8.0,
        label="Specified model · negative second report",zorder=4)[0]
    patch=Patch(facecolor=band_color,edgecolor="#7898B3",linewidth=.8,
        alpha=.9,label="Alternative second reports (shaded)")
    ax.legend(handles=[h1,h2,h3,patch],
        loc="center left",bbox_to_anchor=(.50,.405),
        frameon=True,facecolor="white",edgecolor="#CFD8E3",
        framealpha=.98,fontsize=11.1,handlelength=2.4,
        labelspacing=.55,borderpad=.7)
    ax.set_xlim(-.18,5.4)
    ax.set_ylim(.34,1.09)
    ax.set_xticks(range(6),["Prior","1","2","3","4","5"])
    ax.set_xlabel("Number of detector reports (positive unless noted)")
    ax.set_ylabel("Posterior probability of a stop sign")
    ax.grid(axis="y",alpha=.17)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=.125,right=.985,bottom=.17,top=.97)
    return save(fig,"JNB3-bayesian-updating-integrated",root)


def updating_sequences(root=None):
    style()
    def upd(p,pos):
        a,b=(.9,.2) if pos else (.1,.8)
        return a*p/(a*p+b*(1-p))
    p0=.6;p1=upd(p0,True);p2p=upd(p1,True);p2n=upd(p1,False)
    assert np.isclose(p2p,.96812749,atol=1e-5)
    fig,ax=plt.subplots(figsize=(7.2,3.85))
    ax.plot([0,1,2],[p0,p1,p2p],"-o",color=BLUE,markersize=9,lw=3)
    ax.plot([1,2],[p1,p2n],"--s",color=GOLD,markersize=9,lw=3)
    ax.text(2.06,p2p,f"Positive second report\n{p2p:.3f}",color=BLUE,fontsize=12.5,weight="bold",va="center")
    ax.text(2.06,p2n,f"Negative second report\n{p2n:.3f}",color=GOLD,fontsize=12.5,weight="bold",va="center")
    ax.annotate(f"{p1:.3f}",(1,p1),xytext=(-15,13),textcoords="offset points",fontsize=12,weight="bold")
    ax.annotate(f"{p0:.3f}",(0,p0),xytext=(-10,14),textcoords="offset points",fontsize=12,weight="bold")
    ax.set_xticks([0,1,2],["Prior","First positive","Alternative second report"])
    ax.set_xlim(-.14,2.93);ax.set_ylim(.3,1.07)
    ax.set_ylabel("Probability that stop sign is present")
    ax.grid(axis="y",alpha=.18);fig.subplots_adjust(left=.14,right=.985,top=.95,bottom=.19)
    return save(fig,"JNB3-bayesian-updating-sequences",root)

def updating_bias(root=None):
    style()
    def hist(fpr):
        a=[.6]
        for _ in range(5): a.append(.9*a[-1]/(.9*a[-1]+fpr*(1-a[-1])))
        return np.array(a)
    correct=hist(.2);biased=hist(.05)
    fig,ax=plt.subplots(figsize=(7.2,3.85))
    ax.plot(range(6),correct,"-o",color=BLUE,markersize=7.5,lw=2.9)
    ax.plot(range(6),biased,"--s",color=GOLD,markersize=7.5,lw=2.9)
    ax.annotate("Optimistic assumed model\nfalse-positive rate 0.05",
        xy=(1,biased[1]),xytext=(2.5,.83),color=GOLD,fontsize=12,weight="bold",
        arrowprops=dict(arrowstyle="->",color=GOLD,lw=1.6))
    ax.annotate("Specified model\nfalse-positive rate 0.20",
        xy=(2,correct[2]),xytext=(3.35,.68),color=BLUE,fontsize=12,weight="bold",
        arrowprops=dict(arrowstyle="->",color=BLUE,lw=1.6))
    ax.set_xlim(-.2,5.2);ax.set_ylim(.56,1.085);ax.set_xticks(range(6))
    ax.set_xlabel("Number of successive positive reports");ax.set_ylabel("Posterior probability")
    ax.grid(axis="y",alpha=.18);fig.subplots_adjust(left=.14,right=.98,top=.95,bottom=.2)
    return save(fig,"JNB3-bayesian-updating-bias",root)

def inference_densities(root=None):
    style();x=np.linspace(2,9,600);mu0,v0=5.,1.;z,vr=6.,.5
    v=1/(1/v0+1/vr);mu=v*(mu0/v0+z/vr)
    fig,ax=plt.subplots(figsize=(7.2,4.0))
    prior=norm.pdf(x,mu0,np.sqrt(v0));like=norm.pdf(x,z,np.sqrt(vr))
    posterior=norm.pdf(x,mu,np.sqrt(v))
    ax.plot(x,prior,color=GOLD,lw=2.5,label="Prior")
    ax.plot(x,like,color=TEAL,lw=2.5,ls="-.",label="Likelihood")
    ax.plot(x,posterior,color=BLUE,lw=3.1,label="Posterior")
    ax.fill_between(x,posterior,color=BLUE,alpha=.1)
    for k,c in [(mu0,GOLD),(z,TEAL),(mu,BLUE)]: ax.axvline(k,color=c,lw=1.3,ls=":",alpha=.8)
    ax.annotate("Prior mean\n5.00 m",(5,norm.pdf(5,5,1)),xytext=(3.35,.54),
         fontsize=12.2,color=GOLD,weight="bold",arrowprops=dict(arrowstyle="-",color=GOLD))
    ax.annotate("Measurement\n6.00 m",(6,norm.pdf(6,6,np.sqrt(.5))),xytext=(6.65,.53),
         fontsize=12.2,color=TEAL,weight="bold",arrowprops=dict(arrowstyle="-",color=TEAL))
    ax.annotate("Posterior mean\n5.67 m",(mu,norm.pdf(mu,mu,np.sqrt(v))),xytext=(4.2,.77),
         fontsize=12.2,color=BLUE,weight="bold",arrowprops=dict(arrowstyle="-",color=BLUE))
    ax.set_xlim(2,9);ax.set_ylim(0,.88)
    ax.set_xlabel("Target position (m)");ax.set_ylabel("Density / likelihood (1/m)")
    ax.legend(loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(.5,1.20),fontsize=12)
    ax.grid(axis="y",alpha=.16);fig.subplots_adjust(left=.13,right=.985,top=.80,bottom=.18)
    return save(fig,"JNB4-bayesian-inference-three-densities",root)


def inference_integrated(root=None):
    """Chapter 4 unified Gaussian inference and discrete MAP/MMSE figure."""
    style()
    from matplotlib.lines import Line2D
    plt.rcParams.update({"font.family":"DejaVu Serif"})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(12.4,5.05),
                             gridspec_kw={"width_ratios":[1.12,1]})
    x=np.linspace(2,9,800);mu=17/3;var=1/3
    ax.plot(x,norm.pdf(x,5,1),color=GOLD,lw=2.7,
            label="Prior (mean 5.00 m)")
    ax.plot(x,norm.pdf(x,6,np.sqrt(.5)),color=TEAL,lw=2.7,ls="-.",
            label="Likelihood (center 6.00 m)")
    ax.plot(x,norm.pdf(x,mu,np.sqrt(var)),color=BLUE,lw=3,
            label="Posterior (mean 5.67 m)")
    for val,c in [(5,GOLD),(6,TEAL),(mu,BLUE)]:
        ax.axvline(val,color=c,ls=":",lw=1.6,alpha=.73,zorder=1)
    ax.set_xlim(2.3,8.5);ax.set_ylim(0,.78)
    ax.set_xlabel("Target position, x (m)")
    ax.set_ylabel("Density / likelihood (1/m)")
    ax.set_title("(a)  Gaussian inference",fontsize=15,weight="bold",pad=12)
    ax.legend(loc="upper left",bbox_to_anchor=(.015,.985),fontsize=10.1,
              frameon=False,handlelength=2.5,labelspacing=.5)
    ax.grid(axis="y",alpha=.16)
    states=np.array([0.,1.,3.]);probs=np.array([.2,.5,.3])
    map_x=1.;mmse=float(np.dot(states,probs))
    loss_map=float(np.dot(probs,(states-map_x)**2))
    loss_mmse=float(np.dot(probs,(states-mmse)**2))
    assert np.isclose(mmse,1.4) and np.isclose(loss_map,1.4)
    assert np.isclose(loss_mmse,1.24)
    bx.bar(states,probs,width=.39,color=[TEAL,BLUE,TEAL],alpha=.96,zorder=3)
    for st,p in zip(states,probs):
        bx.text(st,p+.017,f"{p:.2f}",ha="center",va="bottom",
                fontsize=11.2,weight="bold")
    bx.axvline(mmse,color=GOLD,lw=2.2,ls="--",zorder=2)
    bx.set_xlim(-.45,3.52);bx.set_ylim(0,.71)
    bx.set_xticks([0,1,3])
    bx.set_xlabel("Discrete state, x")
    bx.set_ylabel("Posterior probability")
    bx.set_title("(b)  Discrete MAP versus MMSE",fontsize=15,
                 weight="bold",pad=12)
    bx.grid(axis="y",alpha=.16,zorder=0)
    bx.legend(handles=[
        Line2D([0],[0],color=BLUE,lw=8,label="MAP = 1.0 (blue bar)"),
        Line2D([0],[0],color=GOLD,lw=2,ls="--",label="MMSE = 1.4")],
        loc="upper right",frameon=False,fontsize=10.1,handlelength=2.1)
    bx.text(.5,-.30,"Expected squared error",transform=bx.transAxes,
            ha="center",fontsize=12,weight="bold")
    bx.text(.5,-.385,"MAP: 1.40    •    MMSE: 1.24",
            transform=bx.transAxes,ha="center",fontsize=12,color=INK)
    fig.subplots_adjust(left=.078,right=.985,bottom=.30,top=.86,wspace=.31)
    return save(fig,"JNB4-bayesian-inference-integrated",root)

def realtime_latency(root=None):
    style();rng=np.random.default_rng(20261114);n=110
    compute=np.clip(rng.normal(1.8,.13,n),1.43,2.2)
    compute[43:49]=[7.2,6.8,7.5,6.5,6.3,5.8]
    acquired=np.arange(n)*5.;ready=acquired+.8;complete=np.zeros(n)
    for k in range(n):
        complete[k]=max(ready[k],complete[k-1] if k else ready[k])+compute[k]+1
    latency=complete-acquired;missed=latency>4;updates=np.arange(1,n+1)
    assert np.array_equal(updates[missed],np.arange(44,58))
    assert np.isclose(latency.max(),21.9)
    fig,(a,b)=plt.subplots(1,2,figsize=(10.5,4.0),
                             gridspec_kw={"width_ratios":[1,1.35]})
    a.set_title("(a)  Latency budget",weight="bold",fontsize=15,pad=12)
    for start,width,lab,col in [(0,.8,"Sensing\n0.8 ms","#BBD9ED"),
             (.8,2.5,"Computation\n2.5 ms","#F2CC7F"),(3.3,1.,"Reporting\n1.0 ms","#D2EDCC")]:
        a.add_patch(Rectangle((start,-.17),width,.34,facecolor=col,edgecolor=BLUE,lw=1.3))
        a.text(start+width/2,0,lab,ha="center",va="center",fontsize=9.6,weight="bold")
    a.axvline(4,color=RED,ls="--",lw=2);a.axvline(5,color=BLUE,ls=":",lw=1.5)
    a.text(3.95,.44,"Deadline 4 ms",color=RED,ha="right",fontsize=11.8,weight="bold")
    a.text(4.30,.3,"4.3 ms",color=INK,ha="center",fontsize=11)
    a.set_xlim(0,5.2);a.set_ylim(-.44,.55)
    a.set_xlabel("Time since acquisition (ms)");a.set_yticks([])
    a.grid(axis="x",alpha=.12);a.spines["left"].set_visible(False)
    b.set_title("(b)  Delays and deadline misses",weight="bold",fontsize=15,pad=12)
    b.axvspan(43.5,49.5,color=GOLD,alpha=.17)
    b.axhline(4,color=RED,ls="--",lw=2,label="4 ms deadline")
    b.plot(updates,latency,color=BLUE,lw=2.3,label="End-to-end latency")
    b.scatter(updates[missed],latency[missed],s=35,color=RED,zorder=4,label="Deadline misses")
    b.annotate("Slow updates 44–49",xy=(46.5,22),xytext=(55,26),
        fontsize=11.2,color=GOLD,weight="bold",
        arrowprops={"arrowstyle":"->","color":GOLD})
    b.set_xlim(1,110);b.set_ylim(0,27)
    b.set_xlabel("Update number");b.set_ylabel("Latency (ms)")
    b.legend(loc="upper right",frameon=False,fontsize=10)
    b.grid(axis="y",alpha=.16)
    fig.subplots_adjust(left=.085,right=.985,bottom=.21,top=.83,wspace=.34)
    p=save(fig,"JNB6-realtime-latency-final",root)
    return p,{"miss_count":int(missed.sum()),"max_latency_ms":float(latency.max())}

def refresh_figure(topic,root=None):
    fn={"bayes-theorem":bayes_theorem,
        "bayesian-updating-sequences":updating_sequences,
        "bayesian-updating-integrated":updating_integrated,
        "bayesian-updating-bias":updating_bias,
        "bayesian-inference-three-densities":inference_densities,
        "bayesian-inference-integrated":inference_integrated,
        "real-time-bayesian-systems":realtime_latency}[topic]
    return fn(root)
