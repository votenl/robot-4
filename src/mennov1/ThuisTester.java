package mennov1;

import java.io.IOException;

/**
 * 
 * @category Framework
 * 
 * The home testing class for the robot. This initializes a subset of the communication channels (clients) to the bothandler.
 *
 */

public class ThuisTester {

	public static void main(String[] args) {

		EventBus bus = EventBus.getInstance();
		bus.addListener(BotHandler.getInstance());
		bus.addListener(TerminalClient.getInstance());

//		bus.addListener(JabberClient.getInstance());
//		bus.addListener(IrcClient.getInstance());

		// Gebruik de ImageFileClient om een eigen webcam te simuleren
//		bus.addListener(new ImageFileClient("/home/mennov1/webcam/webcam.jpg", 1000L));

		// Als het tweede argument null is, slaat hij het plaatje op zonder te uploaden
//		bus.addListener(new ImageUploader("webcam/capture.jpg", null));
//
//		try {
//			Thread t = new Thread(new WebcamClient());
//			t.start();
//		} catch (Exception e) {}

		// Send a sign of life to robot.uscki.nl
		//System.out.println(SewerSender.sentLifeSign()? "Sent life sign" : "Life sign failed");

		try {
			System.in.read();
		} catch (IOException ex) {
			//ex.printStackTrace();
		}
		//JabberClient.getInstance().disconnect();
	}
}
