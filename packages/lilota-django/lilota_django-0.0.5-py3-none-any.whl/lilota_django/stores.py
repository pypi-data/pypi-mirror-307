from multiprocessing import Lock
from datetime import datetime, UTC
import django
django.setup()
from lilota.stores import TaskStoreBase
from .models import Task


class DjangoTaskStore(TaskStoreBase):

  def __init__(self):
    self._lock = Lock()


  def insert(self, name, description, input):
    self._lock.acquire()
    try:
      task = Task.objects.create()
      task.name = name
      task.description = description
      task.input = input
      task.save()
      return task.id
    finally:
      self._lock.release()


  def get_all_tasks(self):
    self._lock.acquire()
    try:
      return Task.objects.all()
    except Exception as ex:
      return None
    finally:
      self._lock.release()


  def get_by_id(self, id):
    self._lock.acquire()
    try:
      return Task.objects.get(id=id)
    except Exception as ex:
      return None
    finally:
      self._lock.release()


  def set_start(self, id: int):
    self._lock.acquire()
    try:
      task = Task.objects.get(id=id)

      if not task:
        raise Exception(f"The task with the id '{id}' does not exist")
      
      task.start_date_time = datetime.now(UTC)
      task.save()
    finally:
      self._lock.release()

  
  def set_progress(self, id: int, progress: int):
    self._lock.acquire()
    try:
      task = Task.objects.get(id=id)

      if not task:
        raise Exception(f"The task with the id '{id}' does not exist")
      
      task.progress_percentage = progress
      task.save()
    finally:
      self._lock.release()


  def set_output(self, id: int, output: dict):
    self._lock.acquire()
    try:
      task = Task.objects.get(id=id)

      if not task:
        raise Exception(f"The task with the id '{id}' does not exist")
      
      task.output = output
      task.save()
    finally:
      self._lock.release()


  def set_end(self, id: int):
    self._lock.acquire()
    try:
      task = Task.objects.get(id=id)

      if not task:
        raise Exception(f"The task with the id '{id}' does not exist")
      
      task.end_date_time = datetime.now(UTC)
      task.progress_percentage = 100
      task.save()
    finally:
      self._lock.release()
