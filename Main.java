import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class Main {
    public static void main(String[] args) {
        ServerSocket serverSocket;
        Socket clientSocket;
        int port = 5555;
        String address = "192.168.14.182";

        try {
            InetSocketAddress bindAddress = new InetSocketAddress(address, port);
            serverSocket = new ServerSocket();
            serverSocket.bind(bindAddress);

            int currentId = 0;
            String[] pos = {"0:100,100,0;", "1:500,100,180;"};

            while (true) {
                clientSocket = serverSocket.accept(); // Blocking call, waits for a connection
                System.out.println("Connected to: " + clientSocket.getInetAddress());

                Thread clientThread = new Thread(new ClientHandler(clientSocket, currentId, pos));
                clientThread.start();

                currentId = 1;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;
    private int currentId;
    private String[] pos;

    public ClientHandler(Socket clientSocket, int currentId, String[] pos) {
        this.clientSocket = clientSocket;
        this.currentId = currentId;
        this.pos = pos;
    }

    @Override
    public void run() {
        try {
            InputStream input = clientSocket.getInputStream();
            OutputStream output = clientSocket.getOutputStream();

            // Send the current ID to the client
            output.write(String.valueOf(currentId).getBytes("UTF-8"));

            while (true) {
                byte[] buffer = new byte[2048];
                int bytesRead = input.read(buffer);
                if (bytesRead == -1) {
                    output.write("Goodbye".getBytes("UTF-8"));
                    break;
                } else {
                    String reply = new String(buffer, 0, bytesRead, "UTF-8");
                    String[] arr = reply.split(":");
                    int currId = Integer.parseInt(arr[0]);
                    pos[currId] = reply;
                    int nextId = (currId == 0) ? 1 : 0;
                    reply = pos[nextId];
                    output.write(reply.getBytes("UTF-8"));
                }
            }

            System.out.println("Connection Closed");
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}