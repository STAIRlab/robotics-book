"""Small transparent calculations for chapters without a standalone notebook.

Values are either synthetic examples explicitly specified in the manuscript,
recomputations of a printed table (not raw field-data validation), or marked new
synthetic exercises. No measured dataset is manufactured here.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.stats import norm

TOPICS={
'introduction':'A sensing decision with explicit losses',
'bayes-theorem':'Three-location posterior',
'bayesian-updating':'Repeated independent detections',
'bayesian-inference':'Gaussian posterior',
'bayesian-prediction':'Prediction with velocity and acceleration uncertainty',
'real-time-bayesian-systems':'Sampling period and latency budget',
'kalman-filter':'Sequential position updates',
'extended-kalman-filter':'One range-measurement EKF cycle',
'unscented-kalman-filter':'A nonlinear squared transformation',
'bayesian-decision-theory':'Renewal-reward inspection interval',
'probabilistic-robotics':'Discrete condition-state Bayes filter',
'hidden-markov-models':'Forward filtering probabilities',
'bayesian-learning':'Uncertainty in learned sensor bias',
'general-state-space-models':'Filtering and smoothing uncertainty',
'probabilistic-graphical-models':'Exact enumeration on a chain',
'computer-vision':'Displacement uncertainty from coordinate errors',
'slam':'A relative measurement leaves a global gauge unobserved',
'digital-twins':'Gaussian residual calibration',
'infrastructure-applications':'Recomputation of the printed modal-period table',
'conclusions':'Posterior evidence and value of perfect information'}

def gaussian(mu,P,z,R):
    K=P/(P+R)
    return mu+K*(z-mu),(1-K)*P

def examples(topic):
    d={'topic':topic,'title':TOPICS[topic],'data_status':'synthetic illustration'}
    if topic in ['introduction','conclusions']:
        p=np.linspace(0,1,201);evpi=np.minimum(100*p,20)-20*p
        p1=.85*.2/(.85*.2+.1*.8);p2=.85**2*.2/(.85**2*.2+.1**2*.8)
        d.update(values={'posterior_after_one':p1,'posterior_after_two':p2,'EVPI_after_one':20-20*p1,'EVPI_after_two':20-20*p2},x=p,y=evpi,xlabel='Posterior damage probability',ylabel='Expected value of perfect information [loss units]')
    elif topic == 'bayes-theorem':
        prior = np.array([1/3, 1/3, 1/3])
        likelihood = np.array([0.8, 0.4, 0.1])
        
        evidence = np.sum(prior * likelihood)
        posterior = prior * likelihood / evidence
        
        d.update(
            values={
                'prior': prior,
                'likelihood': likelihood,
                'evidence': evidence,
                'posterior': posterior,
            },
            x=np.arange(1, 4),
            y=np.vstack([prior, posterior]),
            labels=['Prior', 'Posterior'],
            xlabel='Candidate robot location',
            ylabel='Probability',
        )
    elif topic=='bayesian-updating':
        p=.6;history=[p]
        for _ in range(5):p=.9*p/(.9*p+.2*(1-p));history.append(p)
        d.update(values={'positive_updates':history,'correlated_two':.7*.3/(.7*.3+.12*.7),'incorrect_independence':.64*.3/(.64*.3+.04*.7)},x=np.arange(6),y=history,xlabel='Conditionally independent positive detections',ylabel='Posterior probability')
    elif topic=='bayesian-inference':
        mu,P=gaussian(5,1,6,.5);x=np.linspace(2,9,300)
        d.update(values={'posterior_mean':mu,'posterior_variance':P},x=x,y=np.vstack([norm.pdf(x,5,1),norm.pdf(x,mu,np.sqrt(P))]),labels=['Prior','Posterior'],xlabel='State',ylabel='Probability density')
    elif topic=='bayesian-prediction':
        t=np.linspace(0,5,101);v=t*t*.04+.25*t**4*.09
        d.update(values={'mean_at_3':1.2*3,'variance_at_3':float(9*.04+.25*81*.09)},x=t,y=np.vstack([t*t*.04,.25*t**4*.09,v]),labels=['Velocity term','Acceleration term','Total'],xlabel='Time [s]',ylabel='Position variance [m^2]')
    elif topic=='real-time-bayesian-systems':
        d.update(values={'sample_period_ms':1000/200,'latency_ms':sum([.8,2.5,1.]),'deadline_ms':4.,'required_reduction_ms':sum([.8,2.5,1.])-4},x=np.arange(1,4),y=np.cumsum([.8,2.5,1.]),xlabel='Sensing, computation, reporting stage',ylabel='Cumulative latency [ms]')
    elif topic=='kalman-filter':
        x,P=0.,1.;means=[x];variances=[P]
        for z in [1.2,2.]:x,P=gaussian(x+1,P+.2,z,.5);means.append(x);variances.append(P)
        d.update(values={'means':means,'variances':variances,'gps_update':gaussian(5,.5,5.2,.2)},x=np.arange(3),y=variances,xlabel='Update count',ylabel='Posterior variance')
    elif topic=='extended-kalman-filter':
        F=np.array([[1.,0,0],[0,1,1],[0,0,1]]);Pp=F@np.diag([.1,.1,.05])@F.T+np.diag([.01,.01,.005]);H=np.array([[-.6,-.8,0]])
        S=float((H@Pp@H.T)[0,0]+.04);K=Pp@H.T/S;P=Pp-K@H@Pp;mean=np.array([1.,0,.1])+K[:,0]*(-.2)
        d.update(values={'predicted_covariance':Pp,'innovation_variance':S,'gain':K[:,0],'posterior_mean':mean,'posterior_covariance':P},x=np.arange(3),y=np.vstack([np.ones(3),np.diag(P)/np.diag(Pp)]),labels=['Prediction','Posterior'],xlabel='State component (x, y, heading)',ylabel='Variance normalized by prediction')
    elif topic=='unscented-kalman-filter':
        x=np.linspace(-3,3,300)
        d.update(values={'normal_1_1_squared_mean':2.,'normal_1_1_squared_variance':6.,'normal_0_1_squared_mean':1.,'normal_0_1_squared_variance':2.},x=x,y=np.vstack([x*x,np.zeros_like(x)]),labels=['Nonlinear measurement x^2','Linearization at zero'],xlabel='State',ylabel='Measurement')
    elif topic=='bayesian-decision-theory':
        a=np.linspace(0,6,6001);S=(1+.01*a**2.5)**-3
        J=(50000*S[1:]+1e6*(1-S[1:]))/cumulative_trapezoid(S,a,initial=0)[1:];idx=np.argmin(J)
        prior=np.array([.8,.2]);loss=np.array([[0.,100.],[12.,12.]])
        current_risk=np.min(loss@prior);perfect_risk=prior@np.min(loss,axis=0)
        evpi=current_risk-perfect_risk
        d.update(values={'optimal_interval':float(a[1:][idx]),'minimum_cost_rate':float(J[idx]),'EVPI':float(evpi),'net_EVPI':float(evpi-3.)},x=a[1:],y=J,xlabel='Renewal interval [years]',ylabel='Expected cost rate [currency/year]',ylim=[0,3e5])
    elif topic=='probabilistic-robotics':
        pred=np.array([[.9,.1],[.05,.95]]).T@np.array([.7,.3]);post=pred*np.array([.15,.8]);post/=post.sum()
        d.update(values={'predicted':pred,'posterior':post},x=np.arange(2),y=np.vstack([pred,post]),labels=['Prediction','After alarm'],xlabel='State (safe=0, damaged=1)',ylabel='Probability')
    elif topic=='hidden-markov-models':
        A=np.array([[.7,.2,.1],[.3,.5,.2],[.2,.3,.5]]);B=np.array([[.5,.4,.1],[.1,.3,.6],[.2,.5,.3]])
        f=np.array([.6,.3,.1])*B[:,1];v=f.copy();filters=[f/f.sum()];back=[]
        for o in [2,0]:
            f=(f@A)*B[:,o];filters.append(f/f.sum());score=v[:,None]*A;back.append(score.argmax(axis=0));v=score.max(axis=0)*B[:,o]
        j=int(v.argmax());path=[j]
        for bp in back[::-1]:j=int(bp[j]);path.append(j)
        path=path[::-1]
        d.update(values={'observation_likelihood':float(f.sum()),'best_path_probability':float(v.max()),'best_path_one_based':[j+1 for j in path],'filtering_distributions':filters},x=np.arange(1,4),y=np.array(filters).T,labels=['s1','s2','s3'],xlabel='Observation step',ylabel='Filtering probability')
    elif topic=='bayesian-learning':
        n=np.arange(0,31);variance=1/(n+1)
        y=np.array([10.4,10.6,10.2]);P=1/(1+len(y));m=P*np.sum(y-10);w=np.array([.12,.04])*np.array([.3,.7]);w/=w.sum()
        d.update(values={'bias_posterior_mean':m,'bias_posterior_variance':P,'predictive_mean':10+m,'predictive_variance':1+P,'Bayes_factor':.12/.04,'posterior_model_probabilities':w},x=n,y=variance,xlabel='Independent calibration measurements',ylabel='Bias posterior variance')
    elif topic=='general-state-space-models':
        # New synthetic finite-data example, with full RTS smoothing.
        observations=np.array([2.,1.5,1.2,1.6,.7]);m,P=2.,1.;ms=[];Ps=[];mp=[];Pp=[]
        for z in observations:
            a=.8*m;v=.8**2*P+.36;mp.append(a);Pp.append(v);m,P=gaussian(a,v,z,.64);ms.append(m);Ps.append(P)
        sm=np.array(ms);sp=np.array(Ps)
        for k in range(3,-1,-1):
            C=Ps[k]*.8/Pp[k+1];sm[k]+=C*(sm[k+1]-mp[k+1]);sp[k]+=C*C*(sp[k+1]-Pp[k+1])
        d.update(values={'first_filter_mean':ms[0],'first_filter_variance':Ps[0],'smoothed_means':sm,'smoothed_variances':sp},x=np.arange(1,6),y=np.vstack([Ps,sp]),labels=['Filtered','Smoothed'],xlabel='Step',ylabel='State variance')
    elif topic=='probabilistic-graphical-models':
        joint=np.zeros((2,2,2))
        for a in range(2):
            for b in range(2):
                for c in range(2):joint[a,b,c]=[.7,.3][a]*([.2,.8][a] if b else 1-[.2,.8][a])*([.1,.9][b] if c else 1-[.1,.9][b])
        post=joint[:,:,1].sum(axis=1)/joint[:,:,1].sum()
        d.update(values={'evidence':float(joint[:,:,1].sum()),'A1_given_C1':float(post[1])},x=np.arange(2),y=np.vstack([[.7,.3],post]),labels=['Prior','After C=1'],xlabel='A state',ylabel='Probability')
    elif topic=='computer-vision':
        sigma=np.linspace(0,2,100);v=.4**2*2*sigma*sigma
        d.update(values={'displacement_mm':.4*(263-250),'variance_mm2':.4**2*2*.5**2,'std_mm':np.sqrt(.4**2*2*.5**2),'interval_mm':[.4*13-1.96*np.sqrt(.4**2*2*.5**2),.4*13+1.96*np.sqrt(.4**2*2*.5**2)]},x=sigma,y=np.sqrt(v),xlabel='Coordinate standard deviation [pixels]',ylabel='Displacement standard deviation [mm]')
    elif topic=='slam':
        # New two-variable illustration, not a mapped trajectory or field trial.
        H=np.array([[-1.,1.]]);prior=np.eye(2);K=prior@H.T/2.1;post=prior-K@H@prior
        gauge=np.array([1.,1.])/np.sqrt(2);relative=np.array([-1.,1.])/np.sqrt(2)
        d.update(values={'prior_covariance':prior,'posterior_covariance':post,'global_shift_variance':float(gauge@post@gauge),'relative_variance':float(relative@post@relative)},x=np.arange(2),y=[float(gauge@post@gauge),float(relative@post@relative)],xlabel='Direction (global shift=0, relative=1)',ylabel='Posterior variance')
    elif topic=='digital-twins':
        mu,P=gaussian(0,.16,.5,.09);x=np.linspace(-1,1,300)
        d.update(values={'discrepancy_posterior_mean':mu,'posterior_variance':P,'predictive_residual_variance':P+.09},x=x,y=np.vstack([norm.pdf(x,0,.4),norm.pdf(x,mu,np.sqrt(P))]),labels=['Prior','Posterior'],xlabel='Model discrepancy [kWh]',ylabel='Probability density')
    elif topic=='infrastructure-applications':
        tm=np.array([.55,.67,.88]);to=np.array([.67,.78,.85]);P=1/(100+tm@tm/.0025);m=P*(100+tm@to/.0025)
        d.update(data_status='recomputation of published manuscript table; raw field measurements not supplied',values={'period_discrepancy_percent':100*(to-tm)/tm,'equivalent_stiffness_ratio':(tm/to)**2,'common_factor_mean':m,'common_factor_variance':P,'updated_periods':m*tm,'residuals':to-m*tm},x=np.arange(1,4),y=np.vstack([tm,to,m*tm]),labels=['Model','Printed observation','Updated common factor'],xlabel='Mode index (NS, EW, torsion)',ylabel='Period [s]')
    else:raise KeyError(topic)
    return d

def to_json(x):
    if isinstance(x,dict):return {k:to_json(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [to_json(v) for v in x]
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    return x

def run_example(topic, root=None):
    """Recompute a chapter example and export natural-size vector PDF and PNG.

    All displayed numbers are returned and written to results/<topic>.json.
    Figure appearance is controlled by the same style as the larger notebooks.
    """
    import matplotlib.pyplot as plt
    import logging
    # cmr10 carries legacy font-table timestamps; this metadata warning is harmless.
    logging.getLogger("fontTools.ttLib.tables._h_e_a_d").setLevel(logging.ERROR)
    from matplotlib.ticker import MaxNLocator
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    plt.style.use(root / 'notebooks' / 'book.mplstyle')
    d = examples(topic)
    x, y = np.asarray(d['x']), np.asarray(d['y'])
    width = 6.5 if topic == 'infrastructure-applications' else 4.6
    fig, ax = plt.subplots(figsize=(width, 3.4), layout='constrained')
    colors = ['#003262', '#B17A00', '#247C86']
    categories = {
        'bayes-theorem': ['1', '2', '3'],
        'real-time-bayesian-systems': ['Sensing', 'Computation', 'Reporting'],
        'extended-kalman-filter': [r'$x$', r'$y$', 'Heading'],
        'probabilistic-robotics': ['Safe', 'Damaged'],
        'probabilistic-graphical-models': [r'$A=0$', r'$A=1$'],
        'slam': ['Global shift', 'Relative'],
        'infrastructure-applications': ['NS', 'EW', 'Torsion'],
    }
    xlabel = {
        'bayesian-updating': 'Independent positive detections',
        'real-time-bayesian-systems': 'Processing stage',
        'extended-kalman-filter': 'State component',
        'probabilistic-robotics': 'Condition state',
        'bayesian-learning': 'Independent calibration measurements',
        'slam': 'State-space direction',
        'infrastructure-applications': 'Mode',
    }.get(topic, d['xlabel'])
    ylabel = {
        'bayesian-prediction': r'Position variance [$\mathrm{m}^2$]',
        'extended-kalman-filter': 'Variance / predicted variance',
        'bayesian-decision-theory': 'Cost rate [thousand currency/year]',
        'computer-vision': 'Displacement SD [mm]',
    }.get(topic, d['ylabel'])
    labels = d.get('labels', [])
    if topic == 'unscented-kalman-filter':
        labels = [r'Nonlinear: $x^2$', 'Linearization at zero']
    if topic == 'hidden-markov-models':
        labels = [r'$s_1$', r'$s_2$', r'$s_3$']
    if topic == 'infrastructure-applications':
        labels = ['Original model', 'Printed observation', 'Updated model']
    categorical = topic in categories
    display_y = y / 1000 if topic == 'bayesian-decision-theory' else y
    if topic == 'bayes-theorem':
        prior, posterior = display_y
        bar_width = 0.20
        
        bars_prior = ax.bar(
            x - bar_width / 2,
            prior,
            width=bar_width,
            color='#A7B4C5',
            label='Prior',
        )
        bars_post = ax.bar(
            x + bar_width / 2,
            posterior,
            width=bar_width,
            color='#003262',
            label='Posterior',
        )
        
        for bars in (bars_prior, bars_post):
            ax.bar_label(
                bars, fmt='%.3f', padding=3, fontsize=8
            )
            
        ax.set_ylim(0, 0.72)
    
    elif categorical and topic != 'real-time-bayesian-systems':

    if categorical and topic != 'real-time-bayesian-systems':
        rows = np.atleast_2d(display_y)
        bar_width = 0.4 / len(rows)
        for i, row in enumerate(rows):
            offset = (i - (len(rows) - 1) / 2) * bar_width
            ax.bar(x + offset, row, width=bar_width, color=colors[i],
                   label=labels[i] if labels else None,
                   hatch=['', '//', '..'][i], edgecolor='white', linewidth=0.6)
        ax.set_ylim(bottom=0)
    elif display_y.ndim == 1:
        ax.plot(x, display_y, marker='o' if len(x) < 10 else None, color=colors[0])
    else:
        for i, row in enumerate(display_y):
            ax.plot(x, row, color=colors[i], ls=['-', '--', '-.'][i],
                    marker=['o', 's', '^'][i] if len(x) < 10 else None,
                    label=labels[i])
    if labels:
        ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015),
                  ncol=3 if width == 6.5 else (2 if len(labels) == 2 else 3),
                  borderaxespad=0, columnspacing=1.0, handlelength=1.8)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    if categorical:
        ax.set_xticks(x, categories[topic])
    elif len(x) < 10:
        ax.set_xticks(x)
    elif topic == 'bayesian-learning':
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
    if 'ylim' in d:
        ax.set_ylim(np.asarray(d['ylim']) / (1000 if topic == 'bayesian-decision-theory' else 1))
    if topic == 'real-time-bayesian-systems':
        ax.axhline(4, ls='--', color=colors[1], lw=1.2)
        ax.text(0.02, 4.04, 'Deadline: 4 ms', transform=ax.get_yaxis_transform(),
                va='bottom', fontsize=9, color=colors[1])
        ax.set_ylim(0, 5)
    if topic == 'bayesian-decision-theory':
        interval = d['values']['optimal_interval']
        cost = d['values']['minimum_cost_rate'] / 1000
        ax.plot(interval, cost, 'o', color=colors[1], zorder=3)
        ax.annotate(f'Minimum at {interval:.3f} years', (interval, cost),
                    xytext=(2.2, 70), arrowprops={'arrowstyle': '-', 'color': colors[1]},
                    color=colors[1], fontsize=9)
    ax.grid(axis='y')
    (root / 'figures').mkdir(exist_ok=True)
    (root / 'results').mkdir(exist_ok=True)
    fig.savefig(root / 'figures' / f'{topic}.pdf',
                metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(root / 'figures' / f'{topic}.png', dpi=200)
    plt.close(fig)
    result = to_json(d)
    (root / 'results' / f'{topic}.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
