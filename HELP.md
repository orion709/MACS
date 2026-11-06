```bash
git config --global user.name "ИМЯ_НА_GITHUB"
git config --global user.email "ПОЧТА_НА_GITHUB"
```
ключ
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "ПОЧТА_НА_GITHUB" -f ~/.ssh/id_ed25519_github
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github
cat ~/.ssh/id_ed25519_github.pub
```

Скопировать выведенный публичный ключ.
GitHub → Settings → SSH and GPG keys → New SSH key → вставить → Add SSH key.

```bash
git config --global core.sshCommand "ssh -i ~/.ssh/id_ed25519_github -o IdentitiesOnly=yes"
ssh -T git@github.com
```

При первом подключении сверить fingerprint: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints
При успехе появится `successfully authenticated`.

```bash
git clone git@github.com:orion709/MACS.git
cd MACS
```
```bash
cd ~/prod/MACS
```

```bash
cd ~/MACS
git status
git add .
git commit -m "Описание изменений"
git push
```

`git add .` добавляет все изменения из текущей папки. Перед коммитом проверить `git status`, чтобы не отправить секреты.

```bash
cd ~/prod/MACS
git pull --ff-only
```

```bash
git status
git diff
git diff --staged
git log --oneline -10
git remote -v
```
Убрать файл из будущего коммита, сохранив правки

```bash
git restore --staged ИМЯ_ФАЙЛА
```
