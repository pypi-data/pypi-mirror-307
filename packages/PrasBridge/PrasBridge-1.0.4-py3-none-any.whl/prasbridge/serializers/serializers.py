"""Module containing the serializers for the models."""
from ..error import pError
from sqlalchemy.ext.declarative import DeclarativeMeta
import warnings
from sqlalchemy import event
from ..error import pWarning

warnings.formatwarning = pWarning

# Deprecated 
class __LifecycleMeta(DeclarativeMeta):
    warnings.warn("This metaclass is deprecated and will be removed in a future release.", DeprecationWarning)
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        
        # Attach event listeners to the class
        event.listen(cls, 'after_insert', __LifecycleMeta._save_after_change)
        event.listen(cls, 'after_update', __LifecycleMeta._save_after_change)

    # Static method to call save on inserts/updates
    @staticmethod
    def _save_after_change(mapper, connection, target):
        if hasattr(target, 'save'):
            target.save()


class SerializerMeta(type):
    def __new__(cls, name, bases, attrs):
        serializers = {}
        for attr_name, attr_value in attrs.items():
            if (attr_name).upper().startswith("PRAS_"):
                identifier = getattr(attr_value, '__identifier__', None)
                if identifier is not None:
                    serializers[identifier] = attr_value
                else:
                    raise pError(f"Serializer '{attr_name}' does not have a '__identifier__' attribute.")

        attrs['_serializers'] = serializers
        return super().__new__(cls, name, bases, attrs)
    

class IntegratedMeta(SerializerMeta, DeclarativeMeta):
    """
    Metaclass that combines the functionality of SerializerMeta and DeclarativeMeta.

    This metaclass allows for the creation of SQLAlchemy models that can also leverage 
    custom serialization capabilities. By inheriting from both SerializerMeta, which manages 
    the registration of multiple serializers within a class, and DeclarativeMeta, which 
    provides the foundational behavior for SQLAlchemy declarative base classes, 
    ComboMeta enables seamless integration of ORM features with dynamic serialization 
    logic.

    With ComboMeta, users can define their SQLAlchemy models and customize their serialization 
    processes within the same class structure, enhancing code organization and reusability.

    This metaclass is required only when you want to use PrasSerializer with SQLAlchemy 
    Base (declarative_base) based models.
    """
    pass


class BaseSerializer:
    def __init__(self, instance, serializer):
        self.instance = instance
        self.serializer = serializer

    def get_fields(self):
        """Extract the fields to serialize from the Meta class."""
        meta = getattr(self.instance.__class__, self.serializer, None)
        if meta is None:
            return None

        if not hasattr(meta, 'fields') or not meta.fields:
            raise ValueError("Meta class must have a 'fields' attribute. Define specific fields or use '__all__'.")
        
        if len(meta.fields) == 1 and '' in meta.fields or None in meta.fields:
            raise ValueError("Meta class must have a 'fields' attribute with at least one valid field defined.")
        
        if '' in meta.fields or None in meta.fields:
            raise ValueError("Invalid field definition in Meta class.")

        fields = meta.fields

        # Return all columns if '__all__' is specified
        if fields == '__all__' or '__all__' in fields:
            return self.instance.__table__.columns.keys() + list(self.instance.__mapper__.relationships.keys())
        else:
            specified_fields = [f for f in fields if not f.startswith('!')]
            excluded_fields = [f[1:] for f in fields if f.startswith('!')]

            if specified_fields:
                return specified_fields
            else:
                if excluded_fields:
                    return [f for f in self.instance.__table__.columns.keys() if f not in excluded_fields]

    def serialize(self):
        """Perform the actual serialization, including related fields."""
        data = {}
        fields = self.get_fields()

        if fields is None:
            return {}

        for field in fields:
            # Check if the field is a relationship
            if field in self.instance.__mapper__.relationships.keys():
                related_value = getattr(self.instance, field)

                # If `related_value` is a list, serialize each item in it
                if isinstance(related_value, list):
                    data[field] = [
                        {col.name: getattr(item, col.name) for col in item.__table__.columns} 
                        for item in related_value
                    ]
                else:
                    # Default serialization for a single relationship
                    data[field] = {col.name: getattr(related_value, col.name) for col in related_value.__table__.columns}
            else:
                # Regular field serialization
                data[field] = getattr(self.instance, field)


        return data
    def serialize_related(self, related_instance, pattern):
        """Serialize a related instance based on user-defined fields."""
        if related_instance is None:
            return None
        
        if pattern.__len__() == 1 and '' in pattern or None in pattern:
            raise ValueError(f"Invalid field definition in Meta class.")
        
        if '' in pattern or None in pattern:
            raise ValueError(f"Invalid field definition in Meta class.")


        # If the pattern is '__all__', serialize all fields
        if pattern == '__all__':
            return {col.name: getattr(related_instance, col.name) for col in related_instance.__table__.columns}

        # Check if specific fields are defined
        if isinstance(pattern, list):
            specified_fields = [field for field in pattern if not field.startswith('!')]
            excluded_fields = [field[1:] for field in pattern if field.startswith('!')]

            if specified_fields:
                data = {}
                for field in specified_fields:
                    if field not in excluded_fields:
                        data[field] = getattr(related_instance, field)
                return data
            else:
                if len(excluded_fields) > 0:
                    # Only exclude fields if no specific fields are defined
                    return {col.name: getattr(related_instance, col.name) for col in related_instance.__table__.columns if col.name not in excluded_fields}

        raise ValueError(f"Invalid pattern format for serialization of {self.serializer}: {pattern}")


class PrasSerializer(metaclass=SerializerMeta):
    def __init__(self, instance):
        
        self.instance = instance

    def to_dict(self, identifier):
        """Return serialized data based on the identifier."""
        serializer_class = self._serializers.get(identifier)
        serializer = serializer_class.__name__


        if serializer_class is None:
            raise ValueError(f"No serializer found for identifier: {identifier}")

        serializer = BaseSerializer(self, serializer) 

        return serializer.serialize()
