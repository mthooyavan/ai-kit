from setuptools import find_packages, setup

setup(
    name="django-ai-kit",
    version="0.1.0",
    description="A Django library that provides abstractions commonly needed for AI projects, including model management, prompt management, chat history management, memory management, and context management.",
    long_description="\n".join(
        [
            open("README.rst", encoding="utf-8").read(),
            open("CHANGES.rst", encoding="utf-8").read(),
        ]
    ),
    keywords="django ai openai bedrock anthropic gemini llm chatbot prompt-engineering azure-openai claude embeddings rag",
    author="Thooyavan Manivaasakar",
    author_email="mail@thooyavan.me",
    maintainer="Thooyavan Manivaasakar",
    maintainer_email="mail@thooyavan.me",
    url="https://github.com/mthooyavan/django-ai-kit",
    project_urls={
        "Documentation": "https://django-ai-kit.readthedocs.io",
        "Source": "https://github.com/mthooyavan/django-ai-kit",
        "Tracker": "https://github.com/mthooyavan/django-ai-kit/issues",
    },
    license="MIT",
    package_dir={"ai_kit": "ai_kit"},
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    # Python version requirement
    python_requires=">=3.10",
    # Dependencies
    install_requires=[
        "Django>=3.2",
        "psycopg2-binary>=2.9",
        "openai>=1.55",
        "anthropic>=0.39",
        "google-generativeai>=0.8",
        "boto3>=1.35",
        "django-model-utils==5.0.0",
        "python-dotenv>=1.0.0",
    ],
    include_package_data=True,
    # Package discovery
    packages=find_packages(exclude=["tests"]),
    # Metadata for PyPI
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    zip_safe=False,
)
