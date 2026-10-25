# SSH into the Spark

This guide connects your computer to the Dell Pro Max GB10 (an NVIDIA DGX Spark) on the Makerspace Wi-Fi. It takes about 5 minutes.

| | |
|---|---|
| Host name | `promaxgb10-8525.local` |
| IP address | `192.168.107.157` (it can change) |
| User | `dell` |
| Wi-Fi | `Frontier:Makerspace` |
| Host key | `SHA256:0PPFdBswY/XUX3BO5JQsEsGhbAiDlpC+yr9IDMM9P2k` (ED25519) |

Your computer must be on the `Frontier:Makerspace` Wi-Fi. The box does not accept connections from other networks.

## 1. Make an SSH key

An SSH key lets you log in without a password. If you already have `~/.ssh/id_ed25519.pub`, skip this step.

Open Terminal (Mac or Linux) or PowerShell (Windows) and run:

```
ssh-keygen -t ed25519
```

Push Enter at each prompt to accept the defaults.

## 2. Get your key onto the box

Do one of the two methods below.

### Method A: send your public key to the owner

1. Print your public key.
   - Mac or Linux: `cat ~/.ssh/id_ed25519.pub`
   - Windows: `type $env:USERPROFILE\.ssh\id_ed25519.pub`
2. Send that one line to the owner. It starts with `ssh-ed25519`.
3. Wait for the owner to say that the key is installed.

The public key is safe to send. Never send the file without `.pub`. That file is your private key.

### Method B: use the password one time

Ask the owner for the password in person. Then run the command below and type the password when it asks.

Mac or Linux:

```
ssh-copy-id dell@promaxgb10-8525.local
```

Windows:

```
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh dell@promaxgb10-8525.local "cat >> ~/.ssh/authorized_keys"
```

## 3. Connect

```
ssh dell@promaxgb10-8525.local
```

The first time, SSH asks "Are you sure you want to continue connecting?" Compare the fingerprint it shows with the host key in the table at the top. If they match, type `yes`.

**Warning:** if the fingerprints do not match, type `no`. Another device could be pretending to be the box.

You see `dell@promaxgb10-8525:~$` when you are in. Type `exit` to leave.

### Optional: a short name

Add these lines to `~/.ssh/config`. Then `ssh spark` connects.

```
Host spark
    HostName promaxgb10-8525.local
    User dell
```

## 4. Use the box

| What | Where or how |
|---|---|
| GPU | NVIDIA GB10, 128 GB of memory shared with the CPU |
| GPU status | `nvidia-smi` |
| CUDA | 13.0 at `/usr/local/cuda`, already on the PATH |
| llama.cpp | `~/src/llama.cpp/build/bin/`, built with CUDA |
| Models | `~/models/` |
| PyTorch | `source ~/.venvs/torch/bin/activate` |

### Keep a job running after you disconnect

Start a `tmux` session before a long job:

```
tmux new -s myjob
```

Push Ctrl-B, then D, to leave the job running. Run `tmux attach -t myjob` to return to it.

### Open a web server from the box in your browser

If a server on the box uses port 8000, connect like this:

```
ssh -L 8000:localhost:8000 dell@promaxgb10-8525.local
```

Then open `http://localhost:8000` on your computer.

### House rules

1. Run `nvidia-smi` before a big job, because another person can use the GPU too.
2. For vLLM, keep `--gpu-memory-utilization` at 0.7 or lower. Above 0.8, the box stalls.
3. Do not change the password or the SSH settings.

## 5. If it does not work

| Error | Fix |
|---|---|
| `No route to host` or `Undefined error: 0` on a Mac | macOS blocks your app from the local network. Use the built-in Terminal app. Or turn on your app in System Settings → Privacy & Security → Local Network. |
| `Could not resolve hostname` | Use the IP address: `ssh dell@192.168.107.157`. If that fails too, ask the owner for the new IP. The owner runs `hostname -I` on the box to find it. |
| `Permission denied (publickey,password)` | The box does not have your key yet. Do step 2 again. |
| The connection times out | Make sure that you are on the `Frontier:Makerspace` Wi-Fi. |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | Stop and ask the owner. Do not delete the warning. |

Written 2026-10-25 for promaxgb10-8525.
