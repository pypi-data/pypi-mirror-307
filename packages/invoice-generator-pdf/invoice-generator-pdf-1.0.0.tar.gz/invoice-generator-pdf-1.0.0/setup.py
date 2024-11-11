from setuptools import setup


setup(
  name = 'invoice-generator-pdf',
  packages = ['invoicing'],
  version = '1.0.0',
  license='MIT',
  description= 'A Python package designed to effortlessly convert Excel-based invoices into professionally formatted '
                'PDF invoices, complete with itemized tables, total calculations, and customizable company branding.',
  author= 'Rishil Shah',
  author_email= 'rishil1211@outlook.com',
  url= 'https://rishil121.vercel.app',
  keywords=[
    'invoice', 'excel', 'pdf', 'generator', 'billing', 'automation',
    'finance', 'reporting', 'invoicing', 'pdf generation', 'data processing',
    'xlsx to pdf', 'business tools', 'accounting', 'sales', 'Python', 'FPDF',
    'PDF creator', 'Excel parser', 'document automation'
  ],
  install_requires=['pandas','fpdf', 'openpyxl'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
