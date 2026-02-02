import os
import re
import sys

def check_campus_isolation(base_dir):
    """
    Checks for illegal imports across sibling subdomains in the Campus domain.
    Rule: A subdomain (e.g., hostel) cannot import from a sibling (e.g., library).
    """
    campus_path = os.path.join(base_dir, "apps", "api", "app", "domains", "campus")
    subdomains = [d for d in os.listdir(campus_path) if os.path.isdir(os.path.join(campus_path, d)) and d != "orchestration" and d != "readmodels"]
    
    violations = []
    
    for sub in subdomains:
        sub_path = os.path.join(campus_path, sub)
        for root, _, files in os.walk(sub_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Find imports from other campus siblings
                        for sibling in subdomains:
                            if sibling == sub:
                                continue
                            
                            # Matches: from app.domains.campus.library, import app.domains.campus.library, etc.
                            pattern = rf"from app\.domains\.campus\.{sibling}|import app\.domains\.campus\.{sibling}|from \.\.\.{sibling}|from \.\.\.\.{sibling}"
                            if re.search(pattern, content):
                                # Check if it's inside TYPE_CHECKING (which is allowed)
                                if "if TYPE_CHECKING:" in content:
                                    # Very naive check - if it's allowed in TC, we might need a more robust parser
                                    # For Phase 1, we just flag it and review
                                    pass
                                
                                violations.append(f"VIOLATION in {full_path}: Illegal import of sibling '{sibling}'")
    
    return violations

if __name__ == "__main__":
    project_root = os.getcwd()
    print(f"Checking Campus Domain Isolation in {project_root}...")
    errors = check_campus_isolation(project_root)
    
    if errors:
        print("\n❌ ARCHITECTURAL DRIFT DETECTED:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("\n✅ Campus Domain isolation is clean.")
        sys.exit(0)
