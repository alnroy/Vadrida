# chat/views.py
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import get_valid_filename
from .models import ChatMessage

def chat_history(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"messages": [], "pinned": []})

    # Get Pinned
    pinned = ChatMessage.objects.filter(is_pinned=True)
    
    # Get Last 100 Messages
    normal = ChatMessage.objects.filter(is_pinned=False).select_related('user').order_by('created_at')
    count = normal.count()
    if count > 100:
        normal = normal[count-100:]

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
    # (Add your unpin logic here if needed)
    pass 

@require_POST
@csrf_exempt
def upload_chat_file(request):
    uploaded = request.FILES.get("file")
    if not uploaded:
        return JsonResponse({"error": "No file"}, status=400)

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