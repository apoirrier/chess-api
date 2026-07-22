from app.schemas.feedback import Feedback
from app.common.feedback_type import FeedbackType

good_feedback = Feedback(type=FeedbackType.SUCCESS, message="")

bad_feedback = Feedback(type=FeedbackType.ERROR, message="")

sicilian_feedback = Feedback(type=FeedbackType.SUCCESS, message="La défense Sicilienne")

french_feedback = Feedback(
    type=FeedbackType.NOBEST,
    message="La défense Française. Jouons plutôt la Défense Sicilienne",
)
