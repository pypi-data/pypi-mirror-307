def find_dependencies(version):
    """
    Find all dependencies of a given project version.

    Args:
        version (dict): Version of the project that needs its dependencies to be determined.

    Returns:
        list: All dependencies as dependency project IDs of the project. Can be empty.
    """
    if not version:
        return f"❌ The provided version is empty."

    deps = []
    try:
        dependency_list = version.get("dependencies")
        for dep in dependency_list:
            deps.append(dep)

        dependency_ids = []
        for dependency in deps:
            dependency_ids.append(dependency.get("project_id"))

        return dependency_ids
    except AttributeError:
        return f"❌ Attribute 'dependencies' not found in version"
    except TypeError:
        return f"❌ A type error has occurred."
