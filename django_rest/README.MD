# What is `APIView`?

`APIView` is the base class in Django REST Framework (DRF) for creating API views.  
It extends Django’s `View` and provides:
- Request parsing (`request.data`, `request.query_params`)
- Content negotiation (JSON, XML, etc.)
- Returns `Response` instead of `HttpResponse`
- Handles authentication and permissions

### Example:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Clothes(APIView):
    def get(self, request):
        clothes = Cloth.objects.all()
        serializer = ClothSerializer(clothes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClothSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
````

✅ You write all the logic manually: query, serialize, save, return response.

---

## 2️⃣ What is `GenericAPIView`?

`GenericAPIView` extends `APIView` and provides helper methods:

* `get_queryset()`
* `get_serializer_class()`
* `get_serializer()`
* `get_object()`
* Handles URL keyword arguments (like `pk`)

### Example:

```python
from rest_framework import generics

class MyView(generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
```

✅ You can now use helpers to simplify code.

---

## 3️⃣ What are Mixins?

DRF mixins provide common actions:

| Mixin                | Method                  | Action        |
| -------------------- | ----------------------- | ------------- |
| `ListModelMixin`     | `list(request)`         | List objects  |
| `CreateModelMixin`   | `create(request)`       | Create object |
| `RetrieveModelMixin` | `retrieve(request, pk)` | Get object    |
| `UpdateModelMixin`   | `update(request, pk)`   | Update object |
| `DestroyModelMixin`  | `destroy(request, pk)`  | Delete object |

---

## 4️⃣ Example: Mixins + GenericAPIView

```python
from rest_framework import mixins, generics

class Clothes(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class ClothDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
```

---

## 5️⃣ What happens under the hood?

### `ListModelMixin.list(request)`

```python
queryset = self.filter_queryset(self.get_queryset())
serializer = self.get_serializer(queryset, many=True)
return Response(serializer.data)
```

### `RetrieveModelMixin.retrieve(request, pk)`

```python
instance = self.get_object()
serializer = self.get_serializer(instance)
return Response(serializer.data)
```

### `GenericAPIView.get_object()`

```python
queryset = self.get_queryset()
pk = self.kwargs.get(self.lookup_field, None)
obj = queryset.get(**{self.lookup_field: pk})
self.check_object_permissions(self.request, obj)
return obj
```

---

## 6️⃣ Difference: APIView vs GenericAPIView + Mixins

| Feature                     | `APIView`  | `GenericAPIView + Mixins` |
| --------------------------- | ---------- | ------------------------- |
| Manual query + serializer   | ✅ Required | ❌ Handled by mixins       |
| Helper methods              | ❌ No       | ✅ Yes                     |
| Boilerplate                 | ✅ High     | ❌ Low                     |
| Customization               | ✅ Full     | ✅ High (can override)     |
| DRY (Don't Repeat Yourself) | ❌ No       | ✅ Yes                     |

---

## 7️⃣ Shortcut: DRF generic views

You can skip mixins + `GenericAPIView` by using:

```python
class Clothes(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class ClothDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
```

---

## 8️⃣ Class hierarchy

```
YourView
│
├── GenericAPIView
│   ├── APIView
│   │   └── Django View
│
├── Mixins
│   ├── ListModelMixin → list()
│   ├── CreateModelMixin → create()
│   ├── RetrieveModelMixin → retrieve()
│   ├── UpdateModelMixin → update()
│   └── DestroyModelMixin → destroy()
```

---

## ✅ Summary

* **APIView**: Use when you want full control and custom logic.
* **GenericAPIView + Mixins**: Use for standard CRUD, avoids repetitive code.
* **DRF generics (`ListCreateAPIView`, etc.)**: The cleanest form for standard APIs.