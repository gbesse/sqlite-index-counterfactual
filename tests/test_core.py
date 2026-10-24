import unittest
from sqlite_index_counterfactual import run
class Tests(unittest.TestCase):
 def data(self):return {'columns':[{'id':'k','type':'INTEGER'},{'id':'v','type':'TEXT'}],'rows':[[i,'v'+str(i)]for i in range(200)],'indexes':[{'id':'key','columns':['k']}],'query':'SELECT v FROM items WHERE k=?','parameters':[71]}
 def test_real_index_changes_plan_preserves_answer(self):
  r=run(self.data())['experiments'];self.assertEqual(r[0]['rows'],[['v71']]);self.assertTrue(r[1]['same_observed_row_bag']);self.assertLess(r[1]['vm_callbacks'],r[0]['vm_callbacks']);self.assertTrue(any('INDEX' in str(row).upper()for row in r[1]['plan']))
 def test_bound_query_cannot_write_or_attach(self):
  for query in ['DELETE FROM items','ATTACH DATABASE ":memory:" AS other','SELECT randomblob(1000000000)']:
   d=self.data();d['query']=query;d['parameters']=[];self.assertTrue(all(r['status']=='query_error'for r in run(d)['experiments']))
 def test_case_insensitive_column_identity_conflict_rejected(self):
  d=self.data();d['columns']=[{'id':'k','type':'TEXT'},{'id':'K','type':'TEXT'}]
  with self.assertRaises(ValueError):run(d)
 def test_budget_does_not_claim_equivalence_of_unfinished_query(self):
  d=self.data();d['vm_step_limit']=20;r=run(d)['experiments'];self.assertEqual(r[0]['status'],'query_error');self.assertIsNone(r[1]['same_observed_row_bag'])
