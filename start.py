import os

#create_account(string creator, string new_account_name, string json_meta, bool broadcast)
#vote(string voter, string author, string permlink, int16_t weight, bool broadcast, string comment_bmchain)
#post_comment(string author, string permlink, string parent_author, string parent_permlink, string title, string body, string json, bool broadcast)
#!/bin/bash
#chmod +x ./setup

def create_chect_vote_limit():
    with open('stress-test-add/check_vote_limit.sh', 'w') as the_file:
        the_file.write('#!/bin/bash\n\n')
        the_file.write('#chmod +x ./check_vote_limit.sh\n\n')
        the_file.write('IFS=$\'\n\'\n')
        the_file.write('post=( $(cat "./post_long") )\n\n')
        the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
        the_file.write('unlock "test"\n')
        for idx in range(0, 100):
            user_idx = str(idx // 10).zfill(3)
            post_idx = str(idx).zfill(3)
            author = 'user800'
            permlink = author + '-post' + post_idx
            parent_author = ''
            parent_permlink = 'bmchain'
            title = permlink
            body = '$post'
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

            voter = 'user810'
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


def create_accounts():
    with open('stress-test-add/create_accounts.sh', 'w') as the_file:
        the_file.write('#!/bin/bash\n\n')
        the_file.write('#chmod +x ./create_accounts.sh\n\n')
        the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
        the_file.write('unlock "test"\n')

        for idx in range(0, 16000):
            creator = 'initminer'
            new_account_name = 'user' + str(idx).zfill(5)
            json_meta = ''
            broadcast = 'true'
            command = 'create_account "' \
                      + creator + '" "' \
                      + new_account_name + '" "' \
                      + json_meta + '" ' \
                      + broadcast + '\n'
            the_file.write(command)

        the_file.write('END')


def create_content_test2():
    for idx_thread in range(0, 8):
        idx_th = str(idx_thread).zfill(2)
        file_name = 'stress-test-02/create_posts' + idx_th + '.sh'

        with open(file_name, 'w') as the_file:
            the_file.write('#!/bin/bash\n\n')
            the_file.write('#chmod +x ./' + file_name + '\n\n')

            for iter in range(0, 10):
                the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
                the_file.write('unlock "test"\n')

                begin = idx_thread * 1000 + iter * 100
                end = (idx_thread * 1000) + iter * 100 + 100
                for idx in range(begin, end):
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
                the_file.write('END\n\n')
                the_file.write('sleep 3s\n\n')


def create_content_test3():
    file_name = ''
    the_file = ''
    author = ''
    post = ''
    comment = ''

    current = get_init_value()

    for idx in range(0, 512000):
        new = get_new_value(idx)
        if new_value('thread', current, new):
            if file_name != '':
                the_file.write('END\n')

            file_name = 'stress-test-03/stress-test' + str(new['thread']).zfill(2) + '.sh'
            the_file = open(file_name, 'w')
            current['thread'] = new['thread']

            the_file.write('#!/bin/bash\n\n')
            the_file.write('#chmod +x ./' + file_name + '\n\n')
            the_file.write('IFS=$\'\\n\'\n')
            the_file.write('post=( $(cat "./post_long") )\n')
            the_file.write('comment=( $(cat "./comment_long") )\n\n')
            the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
            the_file.write('unlock "test"\n')
        elif idx % 860 == 0:
            the_file.write('END\n\n')
            the_file.write('sleep 3s\n\n')
            the_file.write('./cli_wallet --server-rpc-endpoint="ws://127.0.0.1:9876" <<END\n')
            the_file.write('unlock "test"\n')

        if new_value('user', current, new):
            author = 'user' + str(new['user']).zfill(5)
            current['user'] = new['user']
        if new_value('post', current, new):
            post = 'post' + str(new['post']).zfill(2)
            new_post(the_file, author, post)
            current['post'] = new['post']
        if new_value('comment', current, new):
            comment = 'comment' + str(new['comment']).zfill(6)
            comment_author = 'user' + str(new['comment_author']).zfill(5)
            new_comment(the_file, comment_author, comment, author, post)
            current['comment'] = new['comment']
        if new_value('vote', current, new):
            voter = 'user' + str(new['voter']).zfill(5)
            new_vote(the_file, voter, author, post)
            current['vote'] = new['vote']


def get_init_value():
    init = {'thread': -1,
            'user': -1,
            'post': -1,
            'comment': -1,
            'vote': -1,
            'comment_author': -1,
            'voter': -1
            }
    return init


def get_new_value(idx):
    user_per_thread = 2000
    thread = idx // 64000
    comment_author = (thread * user_per_thread) + ((idx // 4) % user_per_thread)
    voter = (thread * user_per_thread) + (idx % user_per_thread)
    new_ = {'thread': thread,
            'user': idx // 32,
            'post': idx // 16,
            'comment': idx // 4,
            'vote': idx,
            'comment_author': comment_author,
            'voter': voter}
    return new_


def new_value(name, current, new_):
    return current[name] != new_[name]


def new_post(the_file, user, post):
    author = user
    permlink = author + '-' + post
    parent_author = ''
    parent_permlink = 'bmchain'
    title = permlink
    body = '$post'
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


def new_comment(the_file, user, comment, post_author, post):
    author = user
    permlink = user + '-' + comment
    parent_author = post_author
    parent_permlink = post_author + '-' + post
    title = permlink
    body = '$comment'
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


def new_vote(the_file, user, author, post):
    voter = user
    permlink = author + '-' + post
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


def main():
    create_accounts()
    #create_content_test2()
    #create_chect_vote_limit()
    create_content_test3()

if __name__ == "__main__":
    main()