# Remote Assist

When automation gets stuck, hand control to a human — open the link on any device to take over, and the agent continues seamlessly when done.

## One Command to Hand Off

```bash
browser-act --session my-task remote-assist --objective "Complete 2FA verification"
```

The CLI returns a live remote URL.

## Take Over from Any Device

The user opens the link in any browser on any device to see the browser screen and operate it:

- Laptop / desktop
- Phone / tablet
- Remote server scenarios (take over from your own device)
- SSH-based remote development

**No headed switch, no same-machine requirement, no software install.** Doesn't depend on screen sharing or VNC — one link, native browser support.

## Typical Scenarios

| Scenario | How it's handled |
|----------|------------------|
| 2FA requiring a phone | The user receives the SMS / app code on the phone and enters it |
| Complex CAPTCHA auto-solve can't handle | Drag-puzzle, behavioral verification, etc. |
| Enterprise SSO with hardware tokens | UKey, dynamic-passcode cards, and other local hardware |
| Mid-workflow human judgment | Picking between candidates, compliance review, sensitive-action confirmation |
| Multi-person collaboration | Send the link to a coworker to complete verification |

## Seamless Continuation After Handoff

After the user finishes:
- No session restart required
- Automation context is not lost
- Browser state, cookies, and current page are all preserved
- The agent picks up from the next step

## Compared to Standard Approaches

| | Standard approach | BrowserAct |
|---|---|---|
| Letting humans intervene during headless | Must switch to headed | Generate a remote URL directly |
| User must be on the same machine | Yes | No |
| Requires extra software (VNC / RDP / screen share) | Yes | No |
| Cross-device handoff | Not supported | Any browser works |
| After the user finishes | Manual session restart | Agent continues automatically |

## Next Steps

- [Better Headless](headless.md) — Default headless + remote handoff philosophy
- [Anti-Blocking](anti-blocking.md) — Try automation before invoking remote-assist
- [Agent Design](agent-design.md) — Design philosophy, automation capabilities, secure by default
