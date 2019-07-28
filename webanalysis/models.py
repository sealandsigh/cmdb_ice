from django.db import models
from django.db import connection

# Create your models here.

class AccessFile(models.Model):
    name = models.CharField(max_length=128,null=False,default='')
    path = models.CharField(max_length=1024,null=False,default='')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

class AccessLog(models.Model):
    file_id = models.IntegerField(null=False,default=0)
    ip = models.GenericIPAddressField(null=False,default="0.0.0.0")
    url = models.CharField(max_length=1024,null=False,default='')
    status_code = models.IntegerField(null=False,default=0)
    access_time = models.DateTimeField(null=False)

    @classmethod
    def dist_status_code(cls,file_id):
        cursor = connection.cursor()
        cursor.execute('''
                                    select status_code, count(*)
                                    from webanalysis_accesslog
                                    where file_id=%s
                                    group by status_code
                                ''', (file_id,))
        rt = cursor.fetchall()
        legend = []
        series = []
        for line in rt:
            legend.append(str(line[0]))
            series.append({"name": str(line[0]), "value": line[1]})

        return legend, series