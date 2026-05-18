🚀 Fluxo completo de merge local

1️⃣ Garante que tudo está salvo

git status
git add .
git commit -m "finaliza feature X"


2️⃣ Atualiza tua branch com o que já existe na main

git fetch origin
git merge origin/main


3️⃣ Resolve conflitos, se houver, e commita

git add .
git commit -m "resolve conflitos com main"


4️⃣ Vai pra main

git checkout main


5️⃣ Atualiza a main local

git pull origin main


6️⃣ Faz o merge da tua branch para a main

git merge nome-da-tua-branch


7️⃣ Sobe pra o repositório remoto

git push origin main


8️⃣ (opcional) Deleta a branch local

git branch -d nome-da-tua-branch