# Aponta para o src.main. Atalho para rodar localmente $ python src/main.py
import asyncio
from src.main import main

if __name__ == "__main__":
    print("Subindo microserviço...")
    asyncio.run(main())