[ludorum](../../README.md) / [environments](./README.md) / grid-world

# Grid World Environment

### Contents:

---

## Usage

For an interesting grid configuration, try the following example:
```bash
python -m main                                                                              \
    play --max-steps 1000                                                                   \
    grid-world                                                                              \
        --rows 10                                                                           \
        --columns 10                                                                        \
        --loss "[(0,9),(9,0)]"                                                             \
        --coins "[(5,4),(5,5),(4,4),(4,5),(8,4),(8,5),(5,1),(4,1),(5,8),(4,8),(1,4),(1,5)]"                                                 \
        --walls "[(1,1),(1,2),(2,1),(8,1),(8,2),(7,1),(1,8),(1,7),(2,8),(8,8),(8,7),(7,8),(3,3),(5,3),(6,3),(6,4),(6,5),(6,6),(4,6),(3,6),(3,5),(3,4)]" \
        --portals "[{'entry': (7,2), 'exit': (2,7)}]"        \
        --render                                                                            \
    q-learning
```