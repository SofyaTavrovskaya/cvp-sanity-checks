import pytest


def test_galera_cluster_status(local_salt_client):
    gs = local_salt_client.cmd(
        'galera:*',
        'cmd.run',
        ['salt-call mysql.status | grep -A1 wsrep_cluster_size | tail -n1'],
        expr_form='pillar')

    if not gs:
        pytest.skip("Galera service or galera:* pillar \
        are not found on this environment.")

    size_cluster = []
    amount = len(gs)

    for item in gs.values():
        size_cluster.append(item.split('\n')[-1].strip())

    assert all(item == str(amount) for item in size_cluster), \
        '''There found inconsistency within cloud. MySQL galera cluster
              is probably broken, the cluster size gathered from nodes:
              {}'''.format(gs)
