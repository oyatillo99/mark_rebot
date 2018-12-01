import psycopg2
import datetime



class DB(object):
                
    def __init__(self, config):
        self.conn = psycopg2.connect(f"host={config.DB_HOST} port=5432\
         user={config.DB_USER} password={config.DB_PASSWORD} dbname={config.DB_NAME}")
        
    def new_user(self, user_id):
        date = datetime.datetime.today()
        
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO users (
                        id,
                        menu_select,
                        group_select,
                        group_count,
                        post_edit_count,
                        date_add,
                        end_msg_id
                    ) 
                    VALUES (%s, 'main_menu', 0, 0, 0, %s, 0)""",(user_id, date,))
                
    def is_user(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT id, menu_select, group_select FROM users WHERE id = {user_id}")
                user =  cur.fetchone()
        return user
        
                    
    def msg_id(self, user_id, msg_id = None ): 
        with self.conn:
            with self.conn.cursor() as cur:
                
                if msg_id:
                    print('DB set msg id: ', msg_id)
                    cur.execute("UPDATE users SET end_msg_id = %s WHERE id = %s;",(msg_id, user_id,))

                else:
                    cur.execute("SELECT end_msg_id from users WHERE id = %s;", (user_id,))
                    msg_id = cur.fetchone()[0]
                    print('DB get msg id: ', msg_id)
        
        return msg_id

    def user_set(self, user_id, set, arg):   
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("UPDATE users SET {} = %s WHERE id = %s;".format(set), (arg, user_id,))

    
    def user_get(self, user_id, get):
        print('USER GET: ', user_id, get)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT {} FROM users WHERE id = %s;".format(get),(user_id,))
                get = cur.fetchone()[0]
        return get


    def get_groups_id(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT id, past_name_ch FROM groups_setting WHERE user_id = {user_id}")
                groups =  cur.fetchall()

        return groups
         

    def new_channel(self, user_id, group_id, channel_title):
        date = datetime.datetime.today()
        channel_title 
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO groups_setting (
                    id,             
                    user_id,
                    post_edit_count,
                    date_add,
                    status,
                    id_photo_mark,
                    text_mark,
                    mark_size,
                    color_mark,
                    position_mark,
                    font_style_mark,
                    past_name_ch
                )
                    VALUES (%s, %s,
                    0, %s ,
                   'on', 'off', 'off', 15, '170 123 120 150',
                    'down_right', 'Raleway', %s);""", (group_id, user_id , date, channel_title,))
        
                cur.execute("""UPDATE users
                    SET group_count = group_count + 1
                    WHERE id = %s;""",(user_id,))


    def get_group(self, ch_id = None, user_id = None):
        if user_id:
            ch_id = self.user_get(user_id, 'group_select')
        
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM groups_setting WHERE id = %s;",(ch_id,))
                group =  cur.fetchone()
        if group:
            return {
                'id'             :group[0],             
                'user_id'        :group[1],
                'post_edit_count':group[2],
                'date_add'       :group[3],
                'status'         :group[4],
                'id_photo_mark'  :group[5],
                'text_mark'      :group[6],
                'mark_size'      :group[7],
                'color_mark'     :group[8],
                'position_mark'  :group[9],
                'font_style_mark':group[10],
                'past_name_ch'   :group[11]   
            }
        else:
            return False
          
    def del_ch_sett(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM groups_setting WHERE id = (select group_select from users where id = %s);",(user_id,))
                cur.execute("""UPDATE users
                    SET group_count = group_count - 1
                    WHERE id = %s;""",(user_id,))

    def switch_status(self, user_id):
         with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT status FROM groups_setting WHERE id = (select group_select from users where id = %s);", (user_id,))
                status = cur.fetchone()[0]
                new_status = 'off' if status == 'on' else 'on'
                print(status, ' -> ', new_status)
                cur.execute("UPDATE groups_setting SET status = %s WHERE id = (select group_select from users where id = %s);", (new_status, user_id,))

    def channel_set(self, user_id, set, arg):
        with self.conn:
            with self.conn.cursor() as cur:
                print('DB channel set:', set, 'arg: ', arg)
                cur.execute("UPDATE groups_setting SET {} = %s \
                WHERE id = (select group_select from users where id = %s);".format(set), (arg, user_id,))



    def get_photo_mark_id(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                group_id = self.user_get(user_id, 'group_select')
                cur.execute("SELECT id_photo_mark FROM groups_setting WHERE id = %s;", (group_id,))
                photo_id = cur.fetchone()[0]
        return photo_id
                                

    def new_edit_post(self, group_id, user_id, type_mark):
        date = datetime.datetime.today()
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO posts (group_id, user_id, type_mark, date_edit)
                    VALUES (%s,%s,%s,%s)""",(group_id, user_id, type_mark, date,))
                cur.execute("""UPDATE users
                    SET post_edit_count = post_edit_count + 1
                    WHERE id = %s;""",(user_id,))
                cur.execute("""UPDATE groups_setting
                    SET post_edit_count = post_edit_count + 1
                    WHERE id = %s;""",(group_id,))   







# CREATE TABLE users (
#     id               int         PRIMARY KEY,
#     menu_select      varchar,
#     group_select     bigint,
#     group_count      int,
#     post_edit_count  int,
#     date_add         timestamp   
# )


# CREATE TABLE IF NOT EXISTS groups_setting (
#     id               int         PRIMARY KEY,
#     user_id          int,
#     post_edit_count  int,
#     date_add         timestamp,
#     status           varchar,
#     id_photo_mark  varchar,
#     text_mark        varchar,
#     mark_size        int,
#     color_mark       varchar,
#     position_mark    varchar,
#     font_style_mark  varchar
# )



# CREATE TABLE IF NOT EXISTS posts (
#     id               serial      PRIMARY KEY,
#     group_id         int,
#     user_id          int,
#     type_mark        varchar,
#     date_edit        timestamp
# )
