package bots;

import mennov1.EventBus;
import events.ReceiveChatEvent;
import events.SendChatEvent;

/**
 * 
 * @author Vincent Tunru
 * @category Bots
 *
 * A very simple example bot who is basically a parrot.
 */
public class Echobot implements IBot<ReceiveChatEvent> {

	public void event(ReceiveChatEvent e) {
		// Answer something cool
		EventBus.getInstance().event(new SendChatEvent(this, e.client, e.sender, "got " + e.message));
	}
}
