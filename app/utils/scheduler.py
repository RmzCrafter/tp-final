from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import timedelta
from app.models.sentiment_model import get_model_instance
from app.config.config import RETRAIN_INTERVAL_DAYS

def init_scheduler():
    """Initialize the scheduler for regular model retraining."""
    scheduler = BackgroundScheduler()
    
    # Schedule model retraining every week
    scheduler.add_job(
        func=retrain_model,
        trigger=IntervalTrigger(days=RETRAIN_INTERVAL_DAYS),
        id='model_retrain_job',
        name='Retrain sentiment analysis model',
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler

def retrain_model():
    """Function to retrain the sentiment analysis model."""
    model = get_model_instance()
    model.retrain_model()
