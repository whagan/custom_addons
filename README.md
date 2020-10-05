# ClickIt
Team ClickIt Github repo.

### Installation

#### Install Odoo

* [Odoo Installation Guide](https://www.odoo.com/documentation/master/setup/install.html#source-install)
    * The installation **WILL NOT WORK** if you are using Python 3.7+. Use Python 3.6.

#### Install Our Module

1. Open a terminal (in administrator mode, if relevant) and move to the top level of your Odoo installation (`odoo-bin` is in the top level).
2. `git clone https://github.com/whagan/custom_addons.git`
3. In your terminal, run the following command:
    * UNIX:  
    `python3 odoo-bin --addons-path=addons,custom_addons -d odoo_db`
    * Windows:   
    `python odoo-bin -w odoo -r odoo --addons-path=addons,custom_addons -d odoo_db`
4. In step 2, we launched odoo with the argument `-d odoo_db`. This allowed odoo to properly initialize, but unfortunately we cannot log in using that database. In your browser, go to `localhost:8069`. 

![Odoo Login Page](https://github.com/jsalajka/images/blob/main/odoo_landing_page.png)

5. On the Odoo login page, click Manage Databases.
6. Create a Master Password, then click "Create Database". 
7. Choose any name for the database EXCEPT `odoo_db`. You will need to check the "Demo Data" box.
8. Stop the odoo process in your terminal. Once it is stopped, run the following command:
    * `git clone https://github.com/whagan/custom_addons.git`
9. Start odoo again with the following command:
    * UNIX:  
    `python3 odoo-bin --addons-path=addons,custom_addons -d DATABASE_NAME -u custom_reports`
    * Windows:  
    `python odoo-bin -w odoo -r odoo --addons-path=addons,custom_addons -d DATABASE_NAME -u custom_reports`  
10. You can now log in with the email and password you chose for the new database.
11. Odoo should open in "Apps". If you are not already in the "Apps" menu, click the Menu button in the top left to open a dropdown menu, then click "Apps".
12. Search "Custom Reports". Click "Install".

#### Activating User Security Groups

13. Go to "Settings". Under "Users", click "Manage Users". 
14. The default is Mitchell Admin. Click "Mitchell Admin".
15. Click "Edit" and check the "Custom Reports / Manager" box.
16. In order for these changes to take effect, you must log out and log back in.

#### Custom Reports

17. Enter "Custom Reports". It should be visible now under the icon in the top left corner.
18. You have now entered the "Custom Reports" module. You may create, edit, or delete the "Report Title", "Url", "Category" and "Description" of a custom report.
19. Under the navbar you may click "Employee Performance Report" and create a new Employee Performance Report. Keep in mind that for the purposes of this Sprint, _the only users who have attendance records who have also made sales_ are users Marc Demo and Mitchell Admin between the dates of August 28 and September 10 of this year.
