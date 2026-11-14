import unittest
import numpy as np
from robotics_book.chapter_examples import examples

class ChapterExamples(unittest.TestCase):
 def test_book_numbers(self):
  expected={'bayesian-inference':{'posterior_mean':17/3,'posterior_variance':1/3},'bayesian-prediction':{'variance_at_3':2.1825},'bayesian-decision-theory':{'optimal_interval':1.074,'EVPI':9.6},'hidden-markov-models':{'observation_likelihood':.02817,'best_path_probability':.00588,'best_path_one_based':[1,1,1]},'bayesian-learning':{'bias_posterior_mean':.3,'posterior_model_probabilities':[.5625,.4375]},'general-state-space-models':{'first_filter_mean':1.8439024390243903,'first_filter_variance':.3902439024390244},'probabilistic-graphical-models':{'evidence':.404,'A1_given_C1':111/202},'computer-vision':{'displacement_mm':5.2,'variance_mm2':.08},'digital-twins':{'discrepancy_posterior_mean':.32,'posterior_variance':.0576},'infrastructure-applications':{'common_factor_mean':1.06380222998,'common_factor_variance':.00140781619552},'conclusions':{'posterior_after_one':.68,'posterior_after_two':.9475409836065574}}
  for topic,checks in expected.items():
   for k,want in checks.items():np.testing.assert_allclose(examples(topic)['values'][k],want,atol=1e-10,rtol=0,err_msg=topic+':'+k)
 def test_gauge_and_smoothing(self):
  v=examples('slam')['values'];self.assertAlmostEqual(v['global_shift_variance'],1.);self.assertAlmostEqual(v['relative_variance'],1/21)
  y=np.asarray(examples('general-state-space-models')['y']);self.assertTrue(np.all(y[1]<=y[0]+1e-12));self.assertTrue(np.all(y[1]>0))

if __name__ == '__main__':
    unittest.main()
