import sqlite3,json,math,re
from .common import integer,identifier,unique_ids

def run(data):
 columns=data['columns'];rows=data['rows'];variants=data['indexes'];unique_ids(columns);unique_ids(variants);names=[r['id']for r in columns]
 if len(set(n.casefold()for n in names))!=len(names)or not 1<=len(columns)<=20 or len(rows)>3000 or len(variants)>10:raise ValueError('bounds')
 for c in columns:
  if not re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',c['id'])or c['type']not in ('INTEGER','TEXT','REAL','BLOB','NUMERIC'):raise ValueError('column')
 for row in rows:
  if len(row)!=len(columns)or any(x is not None and (isinstance(x,bool)or not isinstance(x,(str,int,float))or isinstance(x,(int,float))and(not math.isfinite(x)or abs(x)>1e12)or isinstance(x,str)and len(x)>10000)for x in row):raise ValueError('row')
 for v in variants:
  if not 1<=len(v['columns'])<=len(names)or len(set(v['columns']))!=len(v['columns'])or any(c not in names for c in v['columns']):raise ValueError('index')
 sql=data['query'];params=data.get('parameters',[]);budget=integer(data.get('vm_step_limit',500000),10,2000000)
 if not isinstance(sql,str)or len(sql)>10000 or not isinstance(params,list)or len(params)>100:raise ValueError('query')
 results=[]
 for variant in [None]+variants:
  c=sqlite3.connect(':memory:');steps=[0]
  try:
   c.execute('CREATE TABLE items('+','.join('"'+x['id']+'" '+x['type']for x in columns)+')');c.executemany('INSERT INTO items VALUES ('+','.join('?'for _ in names)+')',rows)
   if variant:c.execute('CREATE INDEX candidate_index ON items('+','.join('"'+x+'"'for x in variant['columns'])+')')
   allowed_functions={'count','sum','avg','min','max','abs','coalesce','ifnull','nullif','length','lower','upper','round','typeof','trim','substr'}
   def auth(action,a,b,db,trigger):
    if action in (sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_RECURSIVE):return sqlite3.SQLITE_OK
    if action==sqlite3.SQLITE_FUNCTION and (b or '').lower()in allowed_functions:return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY
   c.set_authorizer(auth);plan=[list(r)for r in c.execute('EXPLAIN QUERY PLAN '+sql,params)]
   def progress():steps[0]+=1;return int(steps[0]>budget)
   c.set_progress_handler(progress,1);cursor=c.execute(sql,params);answer=cursor.fetchmany(10001)
   if len(answer)>10000:raise ValueError('result_limit')
   if any(isinstance(x,float)and not math.isfinite(x)for r in answer for x in r):raise ValueError('nonfinite_result')
   item={'id':'baseline'if variant is None else variant['id'],'status':'executed','vm_callbacks':steps[0],'plan':plan,'rows':[list(r)for r in answer]}
  except sqlite3.DatabaseError as e:item={'id':'baseline'if variant is None else variant['id'],'status':'query_error','sqlite_code':getattr(e,'sqlite_errorname','SQLITE_ERROR'),'vm_callbacks':steps[0]}
  finally:c.close()
  results.append(item)
 baseline=results[0]
 for r in results[1:]:
  r['same_observed_row_bag']=sorted(json.dumps(x,sort_keys=True)for x in r['rows'])==sorted(json.dumps(x,sort_keys=True)for x in baseline['rows'])if r['status']==baseline['status']=='executed'else None
 return {'experiments':results,'sqlite_version':sqlite3.sqlite_version,'model':'observed_native_vm_callbacks_not_wall_time_or_equivalence_proof'}
