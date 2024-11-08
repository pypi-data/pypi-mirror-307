import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slack-post",
    version="0.1.5",
    author="Fabio Arciniegas",
    author_email="fabio_arciniegas@trendmicro.com",
    description="Post to a slack public channel using a bot token for a slack app capable of doing so.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://dsgithub.trendmicro.com/cloudone-common/slack-post",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':
        ['slack_post=slack_post.slackpost:cli'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires='>=3.6',
    install_requires=[
        'slack_sdk'
    ]
)
