from importlib import resources
import pickle
import os
import requests
import io



import pandas as pnd
import cobra



def get_db(logger):
    
    
    logger.info("Downloading the excel file...")
    sheet_id = "1dXJBIFjCghrdvQtxEOYlVNWAQU4mK-nqLWyDQeUZqek"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    response = requests.get(url)  # download the requested file
    if response.status_code == 200:
        excel_data = io.BytesIO(response.content)   # load into memory
        exceldb = pnd.ExcelFile(excel_data)
    else:
        logger.error(f"Error during download. Please contact the developer.")
        return 1
    
    
    logger.debug("Checking table presence...")
    sheet_names = exceldb.sheet_names
    for i in ['R', 'M', 'authors']: 
        if i not in sheet_names:
            logger.error(f"Sheet '{i}' is missing!")
            return 1
        
        
    logger.debug("Loading the tables...")
    db = {}
    db['R'] = exceldb.parse('R')
    db['M'] = exceldb.parse('M')
    db['authors'] = exceldb.parse('authors')
    
    
    logger.debug("Checking table headers...")
    headers = {}
    headers['R'] = ['rid', 'rstring', 'kr', 'gpr_manual', 'name', 'author', 'notes']
    headers['M'] = ['pure_mid', 'formula', 'charge', 'kc', 'name', 'inchikey', 'author', 'notes']
    headers['authors'] = ['username', 'first_name', 'last_name', 'role', 'mail']
    for i in db.keys(): 
        if set(db[i].columns) != set(headers[i]):
            logger.error(f"Sheet '{i}' is missing the columns {set(headers[i]) - set(db[i].columns)}.")
            return 1
        
    return db
    


    
def introduce_metabolites(logger, db, model):
    
    
    # load assets:
    with resources.path("tsiparser.assets", "idcollection_dict.pickle") as asset_path: 
        with open(asset_path, 'rb') as rb_handler:
            idcollection_dict = pickle.load(rb_handler)

    
    logger.debug("Checking duplicated metabolite IDs...")
    if len(set(db['M']['pure_mid'].to_list())) != len(db['M']): 
        pure_mids = db['M']['pure_mid'].to_list()
        duplicates = list(set([item for item in pure_mids if pure_mids.count(item) > 1]))
        logger.error(f"Sheet 'M' has duplicated metabolites: {duplicates}.")
        return 1
   
        
    # parse M:
    logger.debug("Parsing metabolites...")
    db['M'] = db['M'].set_index('pure_mid', drop=True, verify_integrity=True)
    for pure_mid, row in db['M'].iterrows():
        
        
        # skip empty lines!
        if type(pure_mid) != str: continue
        if pure_mid.strip() == '': continue
        
        
        # parse author
        if pnd.isna(row['author']): 
            logger.error(f"Metabolite '{pure_mid}' has no author.")
            return 1
        for author in row['author'].split(';'):
            author = author.strip()
            if author not in db['authors']['username'].to_list(): 
                logger.error(f"Metabolite '{pure_mid}' has invalid author: '{author}'.")
                return 1
        
        
        # parse formula:
        if pnd.isna(row['formula']):
            logger.error(f"Metabolite '{pure_mid}' has missing formula: '{row['formula']}'.")
            return 1
  
        
        # parse charge: 
        if pnd.isna(row['charge']): 
            logger.error(f"Metabolite '{pure_mid}' has missing charge: '{row['charge']}'.")
            return 1
        
        
        # check if 'kc' codes are real:
        if pnd.isna(row['kc']): 
            logger.error(f"Metabolite '{pure_mid}' has missing KEGG annotation (kc): '{row['kc']}'.")
            return 1
        kc_ids = row['kc'].split(';')
        kc_ids = [i.strip() for i in kc_ids]
        for kc_id in kc_ids:
            if kc_id == 'CXXXXX':  # not in KEGG; could be knowledge gap (e.g. methyl group acceptor in R10404)
                logger.debug(f"Metabolite '{pure_mid}' is not in KEGG ('{kc_id}')!")
                continue  
            if kc_id not in idcollection_dict['kc']:
                logger.error(f"Metabolite '{pure_mid}' has invalid KEGG annotation (kc): '{kc_id}'.")
                return 1
            
            
        # check the existance of the inchikey
        if pnd.isna(row['inchikey']): 
            logger.error(f"Metabolite '{pure_mid}' has missing inchikey: '{row['inchikey']}'.")
            return 1
        # check inchikey format:
        if len(row['inchikey']) != 27 or row['inchikey'][14] != '-' or row['inchikey'][25] != '-':
            logger.error(f"Metabolite '{pure_mid}' has badly formatted inchikey: '{row['inchikey']}'.")
            return 1
        
        
        # add metabolite to model
        m = cobra.Metabolite(f'{pure_mid}_c')
        model.add_metabolites([m])
        m = model.metabolites.get_by_id(f'{pure_mid}_c')
        m.formula = row['formula']
        m.charge = row['charge']
        m.compartment='c'
        # add kc annotations to model
        m.annotation['kegg.compound'] = kc_ids
        
        
    return model
    
    
    
def introduce_reactions(logger, db, model): 
    
    
    # load assets:
    with resources.path("tsiparser.assets", "idcollection_dict.pickle") as asset_path:
        with open(asset_path, 'rb') as rb_handler:
            idcollection_dict = pickle.load(rb_handler)
    
    
    logger.debug("Checking duplicated reaction IDs...")
    if len(set(db['R']['rid'].to_list())) != len(db['R']): 
        pure_mids = db['R']['rid'].to_list()
        duplicates = list(set([item for item in pure_mids if pure_mids.count(item) > 1]))
        logger.error(f"Sheet 'R' has duplicated reactions: {duplicates}.")
        return 1
    
        
    # parse R:
    logger.debug("Parsing reactions...")
    db['R'] = db['R'].set_index('rid', drop=True, verify_integrity=True)
    for rid, row in db['R'].iterrows():
        
        
        # skip empty lines!
        if type(rid) != str: continue
        if rid.strip() == '': continue
        
        
        # parse author
        if pnd.isna(row['author']): 
            logger.error(f"Reaction '{rid}' has no author.")
            return 1
        for author in row['author'].split(';'):
            author = author.strip()
            if author not in db['authors']['username'].to_list(): 
                logger.error(f"Reaction '{rid}' has invalid author: '{author}'.")
                return 1
        
        
        # parse reaction string
        if pnd.isna(row['rstring']): 
            logger.error(f"Reaction '{rid}' has no definition (rstring).")
            return 1
        if ' --> ' not in row['rstring'] and ' <=> ' not in row['rstring']:
            logger.error(f"Reaction '{rid}' has invalid arrow: '{row['rstring']}'.")
            return 1


        # check if 'kr' codes are real:
        if pnd.isna(row['kr']): 
            logger.error(f"Reaction '{rid}' has missing KEGG annotation (kr): '{row['kr']}'.")
            return 1
        kr_ids = row['kr'].split(';')
        kr_ids = [i.strip() for i in kr_ids]
        for kr_id in kr_ids:
            if kr_id not in idcollection_dict['kr']:
                logger.error(f"Reaction '{rid}' has invalid KEGG annotation (kr): '{kr_id}'.")
                return 1
            
            
        # check presence of the GPR
        if pnd.isna(row['gpr_manual']): 
            logger.error(f"Reaction '{rid}' has missing GPR: '{row['gpr_manual']}'.")
            return 1
        
        
        # add reaction to model
        r = cobra.Reaction(rid)
        model.add_reactions([r])
        r = model.reactions.get_by_id(rid)
        r.build_reaction_from_string(row['rstring'])
        for m in r.metabolites:
            if m.formula == None or m.charge == None:
                logger.error(f"Metabolite '{m.id}' appears in '{r.id}' but was not previously defined.")
                return 1
        # add kr annotations to model
        r.annotation['kegg.reaction'] = kr_ids
               
        
        # check if unbalanced
        if r.check_mass_balance() != {}: 
            logger.error(f"Reaction '{r.id}' is unbalanced: {r.check_mass_balance()}.")
            return 1
    
    
    
    return model
    
    
    
    
def check_completeness(logger, model, progress, module, focus): 
    # check KEGG annotations in the universe model to get '%' of completeness per pathway/module.
    
    
    # load assets:
    with resources.path("tsiparser.assets", "summary_dict.pickle") as asset_path: 
        with open(asset_path, 'rb') as rb_handler:
            summary_dict = pickle.load(rb_handler)
    
    
    # get all the 'kr' annotations in the model
    kr_ids_modeled = set()
    for r in model.reactions: 
        for kr_id in r.annotation['kegg.reaction']:
            kr_ids_modeled.add(kr_id)
            
            
    # check if 'focus' exist
    map_ids = set()
    md_ids = set()
    for i in summary_dict:
        map_ids.add(i['map_id'])
        for j in i['mds']:
            md_ids.add(j['md_id'])
    if focus != '-' and focus not in map_ids and focus not in md_ids:
        logger.error(f"The ID provided with --focus does not exist: {focus}.")
        return 1
    if focus.startswith('map'):
        logger.debug(f"With --focus {focus}, --module will switch to False.")
        module = False
    if focus != '-':
        missing_logger = ()
    
                
    
    # define some counters:
    maps_completed = set()
    maps_noreac = set()
    maps_missing = set()
    maps_partial = set()

    
    list_partials  = []
    
    
    # iterate over each map:
    for i in summary_dict:
        
        
        # get ID and name: 
        map_id = i['map_id']
        map_name_short = f"{list(i['map_name'])[0][:20]}"
        if len(list(i['map_name'])[0]) > 20: 
            map_name_short = map_name_short + '...'
        else:  # add spaces as needed: 
            map_name_short = map_name_short + ''.join([' ' for i in range(23-len(map_name_short))])
            
            
        # check if this map was (at least partially) covered:
        missing = i['kr_ids'] - kr_ids_modeled
        present = kr_ids_modeled.intersection(i['kr_ids'])
        if focus == map_id: 
            missing_logger = (map_id, missing)

        
        if missing == set() and i['kr_ids'] != set():
            maps_completed.add(map_id)
            
        elif i['kr_ids'] == set():
            maps_noreac.add(map_id)
            
        elif missing == i['kr_ids']:
            maps_missing.add(map_id)
            
        elif len(missing) < len(i['kr_ids']):
            maps_partial.add(map_id)
            
            # get '%' of completeness:
            perc_completeness = len(present)/len(i['kr_ids'])*100
            perc_completeness_str = str(round(perc_completeness))   # version to be printed
            if len(perc_completeness_str)==1: 
                perc_completeness_str = ' ' + perc_completeness_str
                
            list_partials.append({
                'map_id': map_id,
                'map_name_short': map_name_short, 
                'perc_completeness': perc_completeness,
                'perc_completeness_str': perc_completeness_str,
                'present': present,
                'missing': missing,
                'md_ids': [j['md_id'] for j in i['mds']],
            })
                
            
    # order list by '%' of completness and print:
    list_partials = sorted(list_partials, key=lambda x: x['perc_completeness'], reverse=True)
    for i in list_partials:
        if progress:
            if focus=='-' or focus in i['md_ids'] or focus==i['map_id']:
                logger.info(f"{i['map_id']}: {i['map_name_short']} {i['perc_completeness_str']}% completed, {len(i['present'])} added, {len(i['missing'])} missing.")
        
        
        # get the correspondent pathway element of the 'summary_dict'
        right_item = None
        for k in summary_dict:
            if k['map_id'] == i['map_id']:
                right_item = k
                
                
        # define some counters:
        mds_completed = set()
        mds_noreac = set()
        mds_missing = set()
        mds_partial = set()


        list_partials_md  = []
        spacer = '    '


        # iterate over each module:
        for z in right_item['mds']:


            # get ID and name: 
            md_id = z['md_id']
            md_name_short = f"{list(z['md_name'])[0][:20]}"
            if len(list(z['md_name'])[0]) > 20: 
                md_name_short = md_name_short + '...'
            else:  # add spaces as needed: 
                md_name_short = md_name_short + ''.join([' ' for i in range(23-len(md_name_short))])


            # check if this module was (at least partially) covered:
            missing = z['kr_ids_md'] - kr_ids_modeled
            present = kr_ids_modeled.intersection(z['kr_ids_md'])
            if focus == md_id: 
                missing_logger = (md_id, missing)
            
            
            if missing == set() and z['kr_ids_md'] != set():
                mds_completed.add(md_id)

            elif z['kr_ids_md'] == set():
                mds_noreac.add(md_id)

            elif missing == z['kr_ids_md']:
                mds_missing.add(md_id)

            elif len(missing) < len(z['kr_ids_md']):
                mds_partial.add(md_id)

                # get '%' of completeness:
                perc_completeness = len(present)/len(z['kr_ids_md'])*100
                perc_completeness_str = str(round(perc_completeness))   # version to be printed
                if len(perc_completeness_str)==1: 
                    perc_completeness_str = ' ' + perc_completeness_str

                list_partials_md.append({
                    'md_id': md_id,
                    'md_name_short': md_name_short, 
                    'perc_completeness': perc_completeness,
                    'perc_completeness_str': perc_completeness_str,
                    'present': present,
                    'missing': missing,
                })
               
            
        # order list by '%' of completness and print:
        list_partials_md = sorted(list_partials_md, key=lambda x: x['perc_completeness'], reverse=True)
        for z in list_partials_md:
            if module:
                if focus=='-' or focus==z['md_id']:
                    logger.info(f"{spacer}{z['md_id']}: {z['md_name_short']} {z['perc_completeness_str']}% completed, {len(z['present'])} added, {len(z['missing'])} missing.")
        
        
        # print summary:
        if module and focus=='-':
            logger.info(f"{spacer}Modules of {right_item['map_id']}: completed {len(mds_completed)} - partial {len(mds_partial)} - missing {len(mds_missing)} - noreac {len(mds_noreac)}")
    if focus != '-':
        logger.info(f"Missing reactions focusing on {missing_logger[0]}: {missing_logger[1]}.")
    logger.info(f"Maps: completed {len(maps_completed)} - partial {len(maps_partial)} - missing {len(maps_missing)} - noreac {len(maps_noreac)}")
            
        
    return 0       
            
    

    
    
def tsiparser(args, logger): 
    
    
    if args.progress==False and args.module==True: 
        logger.error(f"You cannot ask --module without --progress (see --help).")
        return 1
    
    if args.progress==False and args.focus!='-':
        logger.error(f"You cannot ask --focus without --progress (see --help).")
        return 1
    
    
    
    # check file structure
    db = get_db(logger)
    if type(db)==int: return 1
                                    
        
    # create the model
    model = cobra.Model('tsiparser_uni')
        
    
    model = introduce_metabolites(logger, db, model)
    if type(model)==int: return 1


    model = introduce_reactions(logger, db, model)
    if type(model)==int: return 1 


    response = check_completeness(logger, model, args.progress, args.module, args.focus)
    if response==1: return 1
    
    
    # output the universe
    cobra.io.save_json_model(model, 'newuni.json')
    logger.info(f"'{os.getcwd()}/newuni.json' created!")
    
    
    
    return 0