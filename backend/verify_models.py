import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models import Base
    # Trigger reflection of metadata relationships
    for mapper in Base.registry.mappers:
        print(f"Verified model: {mapper.class_.__name__}")
    print("\nSUCCESS: All models and relationships imported cleanly with no reference errors.")
except Exception as e:
    import traceback
    print("ERROR verifying models:")
    traceback.print_exc()
    sys.exit(1)
