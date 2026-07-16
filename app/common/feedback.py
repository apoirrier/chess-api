from app.schemas.feedback import Feedback, FeedbackType

good_feedback = Feedback(
    type=FeedbackType.SUCCESS
)

bad_feedback = Feedback(
    type=FeedbackType.ERROR
)

sicilian_feedback = Feedback(
    type=FeedbackType.SUCCESS,
    message="La défense Sicilienne"
)

french_feedback = Feedback(
    type=FeedbackType.NOBEST,
    message="La défense Française. Jouons plutôt la Défense Sicilienne"
)