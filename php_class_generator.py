#! /usr/bin/env python3
from pathlib import Path
from mysql_database import *
from colorama import Fore, Back, Style

from helper_functions import *
from php_class_templates import *


def create_php_dbconfig(mysql_connector: MySQLConnector):
    if mysql_connector.dbconn:
        content = '''
	$host = '{HOST}';
	$uid = '{USERNAME}';
	$pwd = '{PASSWORD}';
	$db = '{DATABASE}';

	$dbconn = new mysqli($host,$uid,$pwd,$db);
	if($dbconn->connect_error){
		die('Error ['.$dbconn->connect_errno.'] '.$dbconn->connect_error);
	}

	$dbconn->set_charset("utf8mb4");
'''.replace(
    '{HOST}', mysql_connector.connection_info.host
).replace(
    '{USERNAME}', mysql_connector.connection_info.username
).replace(
    '{PASSWORD}', mysql_connector.connection_info.password
).replace(
    '{DATABASE}', mysql_connector.connection_info.database
)    

        print(Fore.GREEN + 'Generate database configuration file')
        path = str(Path.home())+'/Output/PHP/'+mysql_connector.connection_info.database+'/classes/dbcfg_'+mysql_connector.connection_info.database+'.php'
        with open(path, 'w') as f:
            f.write('<?php\n')
            f.write(content)
            f.write('?>')
        print('  Completed.')


def create_php_classes(mysql_connector: MySQLConnector, withlogin_info=None):
    if mysql_connector.dbconn:
        create_php_dbconfig(mysql_connector)

        db = Database(mysql_connector, withlogin_info)
        print(mysql_connector.connection_info, end='')
        print(db)

        print('Generate classes')

        tb: DataTable
        for tb in db.datatables:
            table_name = tb.table_name

            # Prepare contents
            column_attr_list = ''
            constructor_attr_list = ''
            array_json_attr_list = ''
            class_properties = ''
            add_attr_list = ''
            add_placeholder = ''
            add_bind_count = ''
            add_bind_params = ''
            addfrompost_attr_checklist = ''
            update_attr_noprimary_list = ''
            update_bind_count = ''
            update_bind_params = ''

            property_ribbon_length = 50

            # {DATABASE_INFO}
            database_info = '''
// SchemaName: {}
// CharacterSet: {}
// Collation: {}
// TableName: {}
// TableEngine: {}
// Version: {}
'''.format(
    db.schema_name,
    db.character_set,
    db.collation,
    tb.table_name,
    tb.engine,
    tb.version
)
            col: DataColumn
            for col in tb.datacolumns:
                # COLUMN_ATTR_LIST
                if column_attr_list != '':
                    column_attr_list += ', '
                column_attr_list += '$'+col.column_name

                # CONSTRUCTOR_ATTR_LIST
                constructor_attr_list += tab(4)+'$this->'+col.column_name+' = $row->'+col.column_name+';\n'

                # {ARRAY_JSON_ATTR_LIST}
                if array_json_attr_list != '':
                    array_json_attr_list += ',\n'
                array_json_attr_list += tab(3)+'"'+col.column_name+'"=>$this->'+col.column_name

                # ADD_ATTR_LIST
                if add_attr_list != '':
                    add_attr_list += ', '
                    add_placeholder += ', '
                    add_bind_params += ',\n'
                add_attr_list += col.column_name

                if db.withlogin_info is not None and db.withlogin_info.password_columnname == col.column_name:
                    add_placeholder += 'PASSWORD(?)'
                else:
                    add_placeholder += '?'

                add_bind_count += 's'
                add_bind_params += tab(4)+'$'+camel_cap(table_name)+'Info->'+col.column_name

                # {UPDATE_ATTR_NOPRIMARY_LIST}
                if not col.is_primary_key:
                    if update_attr_noprimary_list != '':
                        update_attr_noprimary_list += '\n'
                    if db.withlogin_info is not None and db.withlogin_info.password_columnname == col.column_name:
                        update_attr_noprimary_list += tab(4)+'" '+col.column_name+' = PASSWORD(?),".'
                    else:
                        update_attr_noprimary_list += tab(4)+'" '+col.column_name+' = ?,".'

                    if update_bind_params != '':
                        update_bind_params += '\n'
                    update_bind_params += tab(4)+'$'+camel_cap(table_name)+'Info->'+col.column_name+','

                update_bind_count += 's'

                # {CLASS_PROPERTIES}
                class_properties += '''
	//{RIBBONIZED_PROPERTY_NAME}//
    /**
     * Get or Set value of {SCHEMA_NAME}.{COLUMN_NAME}
	 *
	 *<pre>
	 * <b>Usage</b>:
     * &nbsp;&nbsp;<b>Get value</b>
	 * &#9;${CLASS_PRIMARY_KEY_LOWER} = 1;
	 * &#9;${CLASSNAME_LOWER} = new {CLASSNAME}(${CLASS_PRIMARY_KEY_LOWER});
	 * &#9;${COLUMN_NAME_LOWER} = ${CLASSNAME_LOWER}->{COLUMN_NAME}();
     *
     * &nbsp;&nbsp;<b>Set value</b>
	 * &#9;${CLASS_PRIMARY_KEY_LOWER} = 1;
	 * &#9;${CLASSNAME_LOWER} = new {CLASSNAME}(${CLASS_PRIMARY_KEY_LOWER});
	 * &#9;${CLASSNAME_LOWER}->{COLUMN_NAME}(<value to set>);
	 *</pre>
     *
     * @param  {property_datatype}  $value  (optional) Value to set to {SCHEMA_NAME}.{COLUMN_NAME}.
	 * @return  {property_datatype}  Current vaule of {COLUMN_NAME}.
     */
	function {COLUMN_NAME}($value = NULL){
		if(!is_null($value)){
			include "dbcfg_{SCHEMA_NAME}.php";

			// Prepared Statment
			$sql = "UPDATE {TABLE_NAME}".
				" SET {COLUMN_NAME} = {PROPERTY_VALUE}".
				" WHERE {TABLE_PRIMARY_KEY} = ?";

			$stmt = $dbconn->prepare($sql);
			$stmt->bind_param("ss", $value, $this->{TABLE_PRIMARY_KEY});
			$stmt->execute();

			$afr = $stmt->affected_rows;
			if($afr){$this->{COLUMN_NAME} = $value;}	

			$stmt->close();

		}
		return $this->{COLUMN_NAME};

	}//EoFnc
'''.replace(
    '{RIBBONIZED_PROPERTY_NAME}', ribbonize(property_ribbon_length, '*', col.column_name)
).replace(
    '{COLUMN_NAME}', col.column_name
).replace(
    '{PROPERTY_VALUE}', 'PASSWORD(?)' if db.withlogin_info is not None and db.withlogin_info.password_columnname == col.column_name else '?'
).replace(
    '{property_datatype}', db_datatype2php_datatype(col.data_type)
)

                addfrompost_attr_checklist += '''
			${TABLE_NAME}_info->{COLUMN_NAME} = $post_data['{COLUMN_NAME}'];
			if(is_null(${TABLE_NAME}_info->{COLUMN_NAME})){
				$rtrs->Code = 1;
				$rtrs->Value = 0;
				$rtrs->Message = 'Error: Required field "{COLUMN_NAME}" not found or its value is NULL.'; 
				return $rtrs;
			}
'''.replace(
    '{COLUMN_NAME}', col.column_name
)

            # Placeholder replacement
            php_database_info_content = php_database_info.replace('{DATABASE_INFO}', database_info)

            php_helper_classes_content = php_helper_classes.replace('{CLASSNAME}', camel_cap(table_name))
            php_helper_classes_content = php_helper_classes_content.replace('{CLASSNAME_LOWER}', table_name.lower())
            php_helper_classes_content = php_helper_classes_content.replace('{CLASS_PRIMARY_KEY}', camel_cap(table_name)+camel_cap(tb.primary_key))
            php_helper_classes_content = php_helper_classes_content.replace('{CLASS_PRIMARY_KEY_LOWER}', table_name.lower()+'_'+tb.primary_key.lower())
            php_helper_classes_content = php_helper_classes_content.replace('{COLUMN_ATTR_LIST}', column_attr_list)

            # Replace first
            php_main_classes_content = php_main_classes.replace('{CLASS_PROPERTIES}', class_properties)
            php_main_classes_content = php_main_classes_content.replace('{ADDFROMPOST_ATTR_CHECKLIST}', addfrompost_attr_checklist)
            if db.withlogin_info is not None and db.withlogin_info.tablename == table_name:
                php_main_classes_content = php_main_classes_content.replace('{CLASS_WITHLOGIN_CONTENT}', php_class_login)
                php_main_classes_content = php_main_classes_content.replace('{WITHLOGIN_USER_COLUMNNAME}', db.withlogin_info.user_columnname)
                php_main_classes_content = php_main_classes_content.replace('{WITHLOGIN_PASSWORD_COLUMNNAME}', db.withlogin_info.password_columnname)
                php_main_classes_content = php_main_classes_content.replace('{WITHLOGIN_USER_COLUMNNAME_LOWER}', db.withlogin_info.user_columnname.lower())
                php_main_classes_content = php_main_classes_content.replace('{WITHLOGIN_PASSWORD_COLUMNNAME_LOWER}', db.withlogin_info.password_columnname.lower())
            else:
                php_main_classes_content = php_main_classes_content.replace('{CLASS_WITHLOGIN_CONTENT}', '')
                
            # Replace last
            php_main_classes_content = php_main_classes_content.replace('{CLASSNAME}', camel_cap(table_name))
            php_main_classes_content = php_main_classes_content.replace('{CLASSNAME_LOWER}', table_name.lower())
            php_main_classes_content = php_main_classes_content.replace('{CLASS_PRIMARY_KEY}', camel_cap(table_name)+camel_cap(tb.primary_key))
            php_main_classes_content = php_main_classes_content.replace('{CLASS_PRIMARY_KEY_LOWER}', table_name.lower()+'_'+tb.primary_key.lower())
            php_main_classes_content = php_main_classes_content.replace('{COLUMN_ATTR_LIST}', column_attr_list)
            php_main_classes_content = php_main_classes_content.replace('{SCHEMA_NAME}', db.schema_name)
            php_main_classes_content = php_main_classes_content.replace('{TABLE_NAME}', table_name)
            php_main_classes_content = php_main_classes_content.replace('{TABLE_PRIMARY_KEY}', tb.primary_key)
            php_main_classes_content = php_main_classes_content.replace('{CONSTRUCTOR_ATTR_LIST}', constructor_attr_list)
            php_main_classes_content = php_main_classes_content.replace('{ARRAY_JSON_ATTR_LIST}', array_json_attr_list)
            php_main_classes_content = php_main_classes_content.replace('{ADD_ATTR_LIST}', tab(5)+add_attr_list)
            php_main_classes_content = php_main_classes_content.replace('{ADD_PLACEHOLDER}', tab(5)+add_placeholder)
            php_main_classes_content = php_main_classes_content.replace('{ADD_BIND_COUNT}', add_bind_count)
            php_main_classes_content = php_main_classes_content.replace('{ADD_BIND_PARAMS}', add_bind_params)
            php_main_classes_content = php_main_classes_content.replace('{UPDATE_ATTR_NOPRIMARY_LIST}', update_attr_noprimary_list)
            php_main_classes_content = php_main_classes_content.replace('{UPDATE_BIND_COUNT}', update_bind_count)
            php_main_classes_content = php_main_classes_content.replace('{UPDATE_BIND_PARAMS}', update_bind_params)
            
            print(f'Creating {table_name:.<50}', end='')
            path = str(Path.home())+'/Output/PHP/'+mysql_connector.connection_info.database+'/classes/'+camel_cap(table_name)+'Cls.php'
            with open(path, 'w') as f:
                f.write('<?php\n')
                f.write(f'{php_credits}\n')
                f.write(f'{php_database_info_content}\n')
                f.write(f'{php_helper_classes_content}\n')
                f.write(f'{php_main_classes_content}\n')
                f.write('?>')
            state = 'Completed'
            print(f'{state:.>10}')
        print('Generating successful.\n')
        print(Style.RESET_ALL)
        
    else:
        print('Connection to MySQL failed!')