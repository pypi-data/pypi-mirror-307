# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyblade', 'pyblade.backends', 'pyblade.components', 'pyblade.engine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyblade',
    'version': '0.1.7',
    'description': "PyBlade is a lightweight template engine for Python, initially designed for Django. Inspired by Laravel's Blade and Livewire, it simplifies dynamic template creation with developer-friendly @-based directives and component support, all while prioritizing security.",
    'long_description': "# PyBlade\n\n**PyBlade** is an upcoming lightweight, flexible, and efficient template engine for Python, inspired by Laravel's Blade syntax. It aims to make transitioning from Laravel to Django seamless by offering familiar features like components (inspired by **Laravel Livewire**) and a simple, intuitive syntax. Designed primarily for **Django** projects, PyBlade will allow developers to create dynamic, interactive templates with ease, while keeping **security** at the forefront.\n\n## Features (Planned)\n\n- **Familiar Blade-Like Syntax**: Intuitive `@`-based directives for conditions, loops, and variable interpolation.\n- **Component Support**: Inspired by Laravel Livewire, PyBlade will offer component-based templating, allowing developers to create reusable, dynamic components directly within their Django templates.\n- **Easy Django Integration**: Aims to be a powerful alternative to Django's default templating engine, while staying easy to integrate.\n- **Lightweight and Fast**: Focus on performance and simplicity.\n- **Security-Focused**: PyBlade will prioritize security by providing automatic escaping of variables and safe handling of user-generated content to protect against XSS and other common web vulnerabilities.\n- **Ideal for Laravel Developers**: PyBlade is designed to help Laravel developers easily understand and adapt to Django’s ecosystem.\n\n## Custom Template Extension\n\nPyBlade will use a custom template file extension (`.py.html`) to facilitate the development of extensions for text editors. This allows for enhanced features such as:\n\n- **Snippets**: Quickly insert common patterns in your templates.\n- **IntelliSense**: Get suggestions and completions as you type.\n- **Syntax Highlighting**: Color-coded syntax for better readability.\n- **Auto-Completion**: Automatically complete directives and component names.\n- **Additional Extensions**: The ability for developers to create their own extensions for various text editors.\n\nWe aim to provide support for popular text editors such as Visual Studio Code, Sublime Text, Atom and JetBrains IDEs.\nExtensions will be developed to improve usability in these environments.\n\n## Status\n\n**PyBlade** is currently in development and not ready for production use. Key features are still being built, but the project will soon allow developers to experiment with Blade-like templating in Django.\n\n## Installation\n\nOnce released, you will be able to install PyBlade via pip:\n\n```bash\npip install pyblade\n```\n\n## Usage (Coming Soon)\n\nThe usage instructions, including setup and examples for components and directives, will be available once the core features are implemented.\n\n## Security\n\nAt PyBlade, we take security seriously. The template engine will automatically escape output unless explicitly marked as safe. This helps protect against **Cross-Site Scripting (XSS)** and ensures that user-generated content is handled securely. Additional features, such as CSRF token support and other security best practices, will be incorporated to ensure that your Django applications remain secure.\n\n## Contributing\n\nContributions are welcome! PyBlade is an open-source project, and we invite developers from both the Django and Laravel communities to collaborate. Please refer to the [Contributing Guide](CONTRIBUTING.md) for more information.\n\n## Roadmap\n\n- [x] Basic template rendering with variable interpolation\n- [x] Support for conditionals and loops\n- [x] Template inheritance, partials, and slots\n- [x] Integration with Django\n- [ ] Components similar to Laravel Livewire\n- [ ] Security measures\n- [ ] Full documentation\n\n## License\n\nThis project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.\n\n## Acknowledgements\n\n- Inspired by Laravel's Blade template engine and Livewire components.\n- Thanks to the Python, Django, and Laravel communities for their ongoing support of open-source projects.\n- Special thanks to [Michael Dimchuk](https://github.com/michaeldimchuk) for graciously releasing the\nname **PyBlade** on PyPI for this project. Your kindness and support for the open-source community are truly appreciated!\n\n---\nLet's bring the power of Blade-like templating and Livewire-like interactivity to Django ! 🚀\n",
    'author': 'AntaresMugisho',
    'author_email': 'antaresmugisho@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
