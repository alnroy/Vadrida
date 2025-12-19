from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage
from django.views.decorators.http import require_POST
import os
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.text import get_valid_filename



def chat_history(request):
    pinned = ChatMessage.objects.filter(is_pinned=True)
    normal = ChatMessage.objects.filter(is_pinned=False)

    def serialize(m):
        return {
            "id": m.id,
            "user": m.user.user_name,
            "content": m.content,
            "attached_type": m.attached_type,
            "attached_path": m.attached_path,
            "attached_label": m.attached_label,
            "is_pinned": m.is_pinned,
            "time": m.created_at.strftime("%H:%M"),
        }

    return JsonResponse({
        "pinned": [serialize(m) for m in pinned],
        "messages": [serialize(m) for m in normal],
    })

@require_POST
def unpin_message(request):
    msg_id = request.POST.get("id")
    msg = ChatMessage.objects.filter(id=msg_id, is_pinned=True).first()

    if not msg:
        return JsonResponse({"error": "Invalid pin"}, status=400)

    user = request.user_profile

    if msg.user != user and user.role != "admin":
        return JsonResponse({"error": "Not allowed"}, status=403)

    msg.is_pinned = False
    msg.save()

    return JsonResponse({"success": True, "id": msg.id})

@require_POST
@csrf_exempt
def upload_chat_file(request):
    uploaded = request.FILES.get("file")
    if not uploaded:
        return JsonResponse({"error": "No file"}, status=400)

    # ✅ Ensure base folder exists
    base_dir = os.path.join(settings.BASE_DIR, "chat_uploads")
    os.makedirs(base_dir, exist_ok=True)

    safe_name = get_valid_filename(uploaded.name)
    path = os.path.join(base_dir, safe_name)

    with open(path, "wb+") as dest:
        for chunk in uploaded.chunks():
            dest.write(chunk)

    return JsonResponse({
        "path": f"chat_uploads/{safe_name}",
        "label": safe_name
    })
