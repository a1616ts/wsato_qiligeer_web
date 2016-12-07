from django.db import models

OS_CHOICES = (
    ('1', u'centos7'),
    ('2', u'ubuntu1404'),
    ('3', u'opensuse13'),
    ('4', u'debian8'),
)

class Domains(models.Model):
    name = models.CharField('instance name', max_length=45)
    user_id = models.IntegerField('user id')
    server_id = models.IntegerField('serever id')
    size = models.IntegerField('size')
    ram = models.IntegerField('ram')
    vcpus = models.IntegerField('vcpus')
    ipv4_address = models.CharField('ipv4 address', max_length=255, blank=False)
    sshkey_path = models.CharField('sshkey path', max_length=255, blank=False)
    status = models.CharField('status', max_length=45)
    create_date = models.DateField('create date')
    update_date = models.DateField('update_date')
    os = models.CharField(u'OS', max_length = 5, choices = OS_CHOICES)
    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.name
