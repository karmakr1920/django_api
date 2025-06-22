## 1️⃣ What is `APIView`?

`APIView` is the base class in Django REST Framework (DRF) for creating API views.  
It extends Django’s `View` and provides:
- 🚀 Request parsing (`request.data`, `request.query_params`)
- 🚀 Content negotiation (JSON, XML, etc.)
- 🚀 Returns `Response` instead of `HttpResponse`
- 🚀 Handles authentication, permissions, throttling

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
* Handles URL keyword arguments like `pk`
* Supports filtering, pagination, ordering (if you add backends)

### Example:

```python
from rest_framework import generics

class MyView(generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
```

✅ Provides helpers to simplify common tasks.

---

## 3️⃣ What are Mixins?

DRF mixins provide reusable methods for common actions:

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

✅ Mixins provide ready-made methods so you don’t repeat code.

---

## 5️⃣ What are Generic Views (e.g. `ListCreateAPIView`)?

DRF provides **pre-combined generic views** that bundle common mixins:

| Generic View                   | Combines                                                  | Use case               |
| ------------------------------ | --------------------------------------------------------- | ---------------------- |
| `ListAPIView`                  | `ListModelMixin + GenericAPIView`                         | Read-only list         |
| `CreateAPIView`                | `CreateModelMixin + GenericAPIView`                       | Create new object      |
| `RetrieveAPIView`              | `RetrieveModelMixin + GenericAPIView`                     | Retrieve single object |
| `UpdateAPIView`                | `UpdateModelMixin + GenericAPIView`                       | Update object          |
| `DestroyAPIView`               | `DestroyModelMixin + GenericAPIView`                      | Delete object          |
| `ListCreateAPIView`            | `ListModelMixin + CreateModelMixin + GenericAPIView`      | List + create          |
| `RetrieveUpdateAPIView`        | `RetrieveModelMixin + UpdateModelMixin + GenericAPIView`  | Get + update           |
| `RetrieveDestroyAPIView`       | `RetrieveModelMixin + DestroyModelMixin + GenericAPIView` | Get + delete           |
| `RetrieveUpdateDestroyAPIView` | All 3                                                     | Get + update + delete  |

### Example:

```python
from rest_framework import generics

class Clothes(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class ClothDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
```

✅ The cleanest way to create standard CRUD endpoints.

---

## 6️⃣ What happens under the hood?

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

## 7️⃣ Class hierarchy

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
│
└── DRF Generic Views (e.g. ListCreateAPIView)
    └── Combines mixins + GenericAPIView
```

---

## 8️⃣ APIView vs GenericAPIView + Mixins vs Generic Views

| Feature                   | `APIView`  | `GenericAPIView + Mixins` | DRF Generic Views      |
| ------------------------- | ---------- | ------------------------- | ---------------------- |
| Manual query + serializer | ✅ Required | ❌ Handled by mixins       | ❌ Handled internally   |
| Helper methods            | ❌ No       | ✅ Yes                     | ✅ Yes                  |
| Boilerplate               | ✅ High     | ⚠ Medium                  | ❌ Low                  |
| Flexibility               | ✅ Max      | ✅ High                    | ⚠ Can override methods |
| DRY                       | ❌ No       | ✅ Yes                     | ✅ Yes                  |

---

## ✅ Final Notes

* **Use `APIView`** → When you want full control and very custom logic.
* **Use `GenericAPIView + Mixins`** → When you want flexibility but less boilerplate.
* **Use DRF generics (e.g. `ListCreateAPIView`)** → For clean, standard CRUD endpoints.