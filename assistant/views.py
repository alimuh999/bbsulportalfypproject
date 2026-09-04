import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ChatSession, ChatMessage
from .services import ask_deepseek


logger = logging.getLogger(__name__)


@login_required
@require_POST
def chat(request):

    # ======================================================
    # GET AUTHENTICATED STUDENT
    # ======================================================

    try:

        student = request.user.student_profile

    except Exception:

        return JsonResponse(
            {
                "success": False,
                "error": "Student profile not found."
            },
            status=403
        )

    # ======================================================
    # GET MESSAGE
    # ======================================================

    message = (
        request.POST
        .get("message", "")
        .strip()
    )

    if not message:

        return JsonResponse(
            {
                "success": False,
                "error": "Please enter a message."
            },
            status=400
        )

    # ======================================================
    # MESSAGE LIMIT
    # ======================================================

    if len(message) > 2000:

        return JsonResponse(
            {
                "success": False,
                "error": "Message is too long."
            },
            status=400
        )

    # ======================================================
    # GET / CREATE CHAT SESSION
    # ======================================================

    try:

        session = (
            ChatSession.objects
            .filter(student=student)
            .order_by("-updated_at")
            .first()
        )

        if not session:

            session = ChatSession.objects.create(
                student=student
            )

    except Exception as e:

        logger.exception(
            "Chat session error: %s",
            e
        )

        return JsonResponse(
            {
                "success": False,
                "error": "Could not create chat session."
            },
            status=500
        )

    # ======================================================
    # GET PREVIOUS MESSAGES
    # ======================================================

    try:

        previous_messages = (
            session.messages
            .order_by("-created_at")[:10]
        )

        previous_messages = list(
            reversed(previous_messages)
        )

    except Exception as e:

        logger.exception(
            "Chat history error: %s",
            e
        )

        previous_messages = []

    conversation_history = []

    for chat_message in previous_messages:

        role = (
            "user"
            if chat_message.role == "USER"
            else "assistant"
        )

        conversation_history.append({

            "role": role,

            "content": chat_message.message

        })

    # ======================================================
    # SAVE USER MESSAGE
    # ======================================================

    try:

        ChatMessage.objects.create(
            session=session,
            role="USER",
            message=message
        )

    except Exception as e:

        logger.exception(
            "Could not save user message: %s",
            e
        )

    # ======================================================
    # ASK DEEPSEEK
    # ======================================================

    try:

        answer = ask_deepseek(

            student=student,

            message=message,

            conversation_history=conversation_history

        )

    except Exception as e:

        # IMPORTANT:
        # Actual error terminal mein show hoga.

        logger.exception(
            "AI Assistant failed for student %s: %s",
            student.student_id,
            e
        )

        return JsonResponse(
            {
                "success": False,

                "error": (
                    "AI Assistant could not connect "
                    "to DeepSeek. Check the Django "
                    "terminal for the exact error."
                )
            },
            status=500
        )

    # ======================================================
    # SAVE AI RESPONSE
    # ======================================================

    try:

        ChatMessage.objects.create(

            session=session,

            role="ASSISTANT",

            message=answer

        )

    except Exception as e:

        logger.exception(
            "Could not save AI response: %s",
            e
        )

    # ======================================================
    # SUCCESS RESPONSE
    # ======================================================

    return JsonResponse(
        {
            "success": True,
            "answer": answer
        }
    )