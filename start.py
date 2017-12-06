import os

#create_account(string creator, string new_account_name, string json_meta, bool broadcast)
#vote(string voter, string author, string permlink, int16_t weight, bool broadcast, string comment_bmchain)
#post_comment(string author, string permlink, string parent_author, string parent_permlink, string title, string body, string json, bool broadcast)
#!/bin/bash
#chmod +x ./setup


def create_accounts():
    with open('create_accounts.sh', 'w') as the_file:
        the_file.write('#!/bin/bash\n\n')
        the_file.write('#chmod +x ./create_accounts.sh\n\n')
        the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
        the_file.write('unlock "test"\n')

        for idx in range(0, 1000):
            creator = 'initminer'
            new_account_name = 'user' + str(idx).zfill(3)
            json_meta = ''
            broadcast = 'true'
            command = 'create_account "' \
                      + creator + '" "' \
                      + new_account_name + '" "' \
                      + json_meta + '" ' \
                      + broadcast + '\n'
            the_file.write(command)

        the_file.write('END')


def create_content():
    for idx_thread in range(0, 8):
        idx_th = str(idx_thread).zfill(2)
        file_name = 'create_posts' + idx_th + '.sh'

        with open(file_name, 'w') as the_file:
            the_file.write('#!/bin/bash\n\n')
            the_file.write('#chmod +x ./' + file_name + '\n\n')
            the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
            the_file.write('unlock "test"\n')

            for idx in range(idx_thread * 1000, (idx_thread * 1000) + 1000):
                user_idx = str(idx // 10).zfill(3)
                post_idx = str(idx % 10).zfill(3)
                author = 'user' + user_idx
                permlink = author + '-post' + post_idx
                parent_author = ''
                parent_permlink = 'bmchain'
                title = permlink
                body = permlink
                json_meta = ''
                broadcast = 'true'
                command = 'post_comment "' \
                          + author + '" "' \
                          + permlink + '" "' \
                          + parent_author + '" "' \
                          + parent_permlink + '" "' \
                          + title + '" "' \
                          + body + '" "' \
                          + json_meta + '" ' \
                          + broadcast + '\n'
                the_file.write(command)
                # vote(string voter, string author, string permlink, int16_t weight, bool broadcast, string comment_bmchain)
                for idx_v in range(idx_thread * 100, (idx_thread * 100) + 100):
                    voter = 'user' + str(idx_v).zfill(3)
                    weight = '100'
                    broadcast = 'true'
                    comment_bmchain = ''
                    command_v = 'vote "' \
                                + voter + '" "' \
                                + author + '" "' \
                                + permlink + '" ' \
                                + weight + ' ' \
                                + broadcast + ' "' \
                                + comment_bmchain + '"\n'
                    the_file.write(command_v)
            the_file.write('END')



def main():
    #create_accounts()
    create_content()


if __name__ == "__main__":
    main()