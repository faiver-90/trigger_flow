from celery import shared_task


@shared_task(name="sync_articles")
def sync_articles():
    print("Syncing articles...")
