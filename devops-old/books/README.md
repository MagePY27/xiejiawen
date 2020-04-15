#### 数据库模型
```python
from django.db import models

# 出版商表结构
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)

    def __str__(self):
        return self.name

# 作者信息表的结构
class Author(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return self.name

# 书的表结构
class Book(models.Model):
    title = models.CharField(max_length=100,help_text="书名")
    # 作者和书是多对多的关系
    authors = models.ManyToManyField(Author,verbose_name="作者", help_text="作者")
    # 一本书只能被一家出版，出版商可以出版多本书
    publisher = models.ForeignKey(Publisher,verbose_name="出版社", help_text="出版社", on_delete=models.CASCADE)


    def __str__(self):
        return self.title
```

#### 进入ipython模式操作数据
```
python manage.py shell

from books.models import Publisher,Book,Author
```
```python
p = {'id':1,'name':'清华大学出版社', 'address':'清华大学'}
Publisher.objects.create(**p)

a = {'name':'韩寒', 'email':'hanhan@qq.com'}
Author.objects.create(**a)

#添加出版社
b = {'title':'平凡的世界', 'publisher_id':1} #这种方式不常用，并且存在风险（publisher_id可能不存在）
Book.objects.create(**b) 

p = Publisher.objects.get(pk=2) #这种外键方式比较常用
p
b = {'title':'斗罗大陆', 'publisher':p}
Book.objects.create(**b)

#对书本添加作者
a = Author.objects.get(id=1)
a
b = Book.objects.get(id=1)
b
b.authors.add(a)
#再添加一个作者
a2 = Authors.objects.get(id=2)
b.authors.add(a2)
b.authors.all() #列出所有作者

a_list = Author.objects.filter(id__lt=1)
a_list
b.authors.add(*a_list) #列表需要解构，因此需要带*号
b #这种添加方式为直接添加，对于相同的选项不覆盖
```
**add方式和se方式**
1.add追加，set覆盖(先将列表清空然后再添加)
2.add支持列表和对象，set支持列表
3.add(*list), set(list)


#### 对作者添加书籍
```
a = Author.objects.get(id=1)
b = Book.objects.get(id=1)
```
正向查找：#以书为切入口来查找作者
```b.authors.all() ```
反向查找：#以作者为切入口来查找书籍
```a.book_set.all()```
#带关联字段的表成为主表（book），不带关联字段的表为从表（author）


**添加**
```python
b=Book.objects.get(id=2)
a.book_set.add(b) #添加书对象
b_list = Book.objects.filter(id__gt=2) #id大于2的书的列表
a.book_set.add(*b_list)
```

#### 总结：
**正向添加，查找**
```
1.查询主表的一条记录
b = Book.objects.get(id=1)
2.从从表中查询出需要添加的对象
a = Author.objects.get(id=1)
3.将这个对象添加/追加给这个主表
b.authors.add(a)
```
**添加多个对象**
```
4.查询从表中的多个对象
a_list = Author.objects.filter(id__gt=2) #id大于2的作者
5.两种方式添加（add, set)
b.authors.add(*a_list) #追加
b.authoes.set(a_list) #覆盖，不需要参数解构
```
#### 正向查询
**主表对象.从表关联字段.all()**
b.authors.all()

#### 反向添加，查询
```
a.book_set.add()
a.book_set.all()
```


#### 查询所有
books = Book.objects.values('title', 'publisher__name', 'publisher__city', 'authors__name', 'authors__email')
books
books=Book.objects.values('title','               
    'publisher__name',       # 正向外健:外键字段___对应从表字段
    'authors__name',         # 正向多对多：关联字段_对应从表字段
    'authors__email',   
    )
#### 反向查找
pub = Publisher.objects.values('name','city','book__title') #book主表__title



#### 通用视图
