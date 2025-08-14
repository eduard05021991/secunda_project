#!/bin/bash

# Находим и удаляем все папки __pycache__ в текущей директории и поддиректориях
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Все папки __pycache__ были удалены."
