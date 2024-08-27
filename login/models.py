
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # ckeditor.widgets yerine ckeditor.fields kullanılmalı
from django.utils.text import slugify

class Reader(models.Model):
    user = models.ForeignKey(User, verbose_name="Kullanıcı", on_delete=models.SET_NULL, null=True,related_name='readers')
    phone = models.CharField(verbose_name="Telefon", max_length=50)
    is_darkmode = models.BooleanField(verbose_name="Dark Mode", default=False)
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Son Güncelleme Tarihi", auto_now=True, auto_now_add=False)

    is_delete = models.BooleanField(verbose_name="Silindi", default=False)
    is_reader=models.BooleanField(default=False)
    delete_date = models.DateTimeField(verbose_name="Silinme Tarihi", blank=True, null=True)
    slug = models.SlugField(verbose_name="Url", unique=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return self.user.username
        
    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.user.first_name} {self.user.last_name}"
            full_name = full_name.replace('ı', 'i')
            proposed_slug = slugify(full_name)
            if Reader.objects.filter(slug=proposed_slug).exists():
                counter = 1
                while True:
                    new_slug = f"{proposed_slug}-{counter}"
                    if not Reader.objects.filter(slug=new_slug).exists():
                        proposed_slug = new_slug
                        break
                    counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)

class Author(models.Model):
    ROLE_CHOICES = (
        ('Backend Developer', 'Backend Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Fullstack Developer', 'Fullstack Developer'),
        ('Web Developer', 'Web Developer'),
        ('Mobile Developer', 'Mobile Developer'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('UI/UX Designer', 'UI/UX Designer'),
        ('Graphic Designer', 'Graphic Designer'),
        ('Quality Assurance Engineer', 'Quality Assurance Engineer'),
        ('Project Manager', 'Project Manager'),
        ('Product Manager', 'Product Manager'),
        ('Scrum Master', 'Scrum Master'),
        ('Database Administrator', 'Database Administrator'),
        ('System Administrator', 'System Administrator'),
        ('Network Administrator', 'Network Administrator'),
        ('Technical Support', 'Technical Support'),
        ('Customer Support', 'Customer Support'),
        ('Sales Manager', 'Sales Manager'),
        ('HR Manager', 'HR Manager'),
        ('Finance Manager', 'Finance Manager'),
        ('Legal Advisor', 'Legal Advisor'),
        ('Content Writer', 'Content Writer'),
        ('Marketing Specialist', 'Marketing Specialist'),
        ('Business Analyst', 'Business Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('Security Specialist', 'Security Specialist'),
        ('IT Consultant', 'IT Consultant'),
        ('Trainer / Instructor', 'Trainer / Instructor'),
        ('Intern', 'Intern'),
    )
    role = models.CharField(verbose_name="Görevi", max_length=50, choices=ROLE_CHOICES)
    user = models.ForeignKey(User, verbose_name="Kullanıcı", on_delete=models.SET_NULL, null=True, related_name='authors')
    author_about = models.CharField(verbose_name="Yazar Hakkında", max_length=100, default="")
    phone = models.CharField(verbose_name="Telefon", max_length=50)
    is_darkmode = models.BooleanField(verbose_name="Dark Mode")
    is_delete = models.BooleanField(verbose_name="Silindi", default=False)
    delete_date = models.DateTimeField(verbose_name="Silinme Tarihi", blank=True, null=True)
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Son Güncelleme Tarihi", auto_now=True, auto_now_add=False)
    slug = models.SlugField(verbose_name="Url", unique=True, editable=False)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return self.user.username
        
    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.user.first_name} {self.user.last_name}"
            proposed_slug = slugify(full_name)
            if Author.objects.filter(slug=proposed_slug).exists():
                counter = 1
                while True:
                    new_slug = f"{proposed_slug}-{counter}"
                    if not Author.objects.filter(slug=new_slug).exists():
                        proposed_slug = new_slug
                        break
                    counter += 1
            self.slug = proposed_slug
        super().save(*args, **kwargs)

class Contract(models.Model):
    title = models.CharField(verbose_name="Başlık", max_length=50)
    content = RichTextField()
    is_delete = models.BooleanField(verbose_name="Silindi", default=False)
    delete_date = models.DateTimeField(verbose_name="Silinme Tarihi", blank=True, null=True)
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Son Güncelleme Tarihi", auto_now=True, auto_now_add=False)
    slug = models.SlugField(verbose_name="Url", unique=True, editable=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            proposed_slug = slugify(self.title)
            self.slug = proposed_slug
        super().save(*args, **kwargs)

class ContractVerified(models.Model):
    customer = models.ForeignKey(Reader, verbose_name="Müşteri", on_delete=models.SET_NULL, null=True)
    contracts = models.ManyToManyField(Contract, verbose_name="Sözleşmeler")
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Son Güncelleme Tarihi", auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.customer.user.first_name and self.customer.user.last_name:
            return f"{self.customer.user.first_name} {self.customer.user.last_name} Sözleşmeleri"
        else:
            return f"{self.customer.user.username} Sözleşmeleri"
        
class ContactVerified(models.Model):
    customer = models.ForeignKey(Reader, verbose_name="Müşteri", on_delete=models.SET_NULL, null=True)
    is_phone = models.BooleanField(verbose_name="Telefon Doğrulandı", default=False)
    is_mail = models.BooleanField(verbose_name="Mail Doğrulandı", default=False)
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Son Güncelleme Tarihi", auto_now=True, auto_now_add=False)
    is_delete = models.BooleanField(verbose_name="Silindi", default=False)
    delete_date = models.DateTimeField(verbose_name="Silinme Tarihi", blank=True, null=True)

    def __str__(self):
        if self.customer.user.first_name and self.customer.user.last_name:
            return f"{self.customer.user.first_name} {self.customer.user.last_name} İletişim Doğrulaması"
        else:
            return f"{self.customer.user.username} İletişim Doğrulaması"

class UserLog(models.Model):
    user = models.ForeignKey(User, verbose_name="Kullanıcı", on_delete=models.SET_NULL, null=True)
    action = models.CharField(verbose_name="İşlem", max_length=1024)
    created_date = models.DateTimeField(verbose_name="Oluşturma Tarihi", auto_now=False, auto_now_add=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name} Logları"
        else:
            return f"{self.user.username} Logları"
    


