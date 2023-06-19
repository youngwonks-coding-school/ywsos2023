import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'api_interface.dart';
import 'utils.dart';

class Authenticate extends StatefulWidget {
  const Authenticate({super.key, required this.title});

  final String title;
  final selectedColor = const Color.fromRGBO(249, 181, 12, 1);
  final unSelectedColor = const Color.fromRGBO(88, 47, 195, 1);

  @override
  State<Authenticate> createState() => _AuthenticateState();
}

class _AuthenticateState extends State<Authenticate> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    // Clean up the controller when the widget is removed from the
    // widget tree.
    emailController.dispose();
    passwordController.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appbarComponent(title: widget.title),
      resizeToAvoidBottomInset: true,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              buildTextField(
                labelText: "Email",
                controller: emailController,
                obscureText: false,
                icon: Icons.email,
                context: context,
              ),
              const SizedBox(height: 5),
              buildTextField(
                labelText: "Password",
                controller: passwordController,
                obscureText: true,
                icon: Icons.lock,
                context: context,
              ),
              const SizedBox(height: 6),
              ElevatedButton.icon(
                onPressed: () async {
                  Response response = await API()
                      .login(emailController.text, passwordController.text);
                  if (response.statusCode! < 400) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Successfully logged in!'),
                      ),
                    );
                    Navigator.of(context).pushNamed('/');
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content:
                            Text('Your email or password is incorrect!'),
                      ),
                    );
                  }
                },
                icon: const Icon(Icons.login, size: 19),
                label: const Text("Login", style: TextStyle(fontSize: 16)),
              ),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                child: Row(
                  children: [
                    Expanded(
                      child: Divider(
                        color: Colors.black,
                        thickness: 1,
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 8),
                      child: Text('OR'),
                    ),
                    Expanded(
                      child: Divider(
                        color: Colors.black,
                        thickness: 1,
                      ),
                    ),
                  ],
                ),
              ),
              ElevatedButton.icon(
                onPressed: () async {
                  Response response = await API()
                      .register(emailController.text, passwordController.text);
                  if (response.statusCode! < 400) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Successfully registered!'),
                      ),
                    );
                    Navigator.of(context).pushNamed('/');
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content:
                            Text('An account with that email already exists!'),
                      ),
                    );
                  }
                },
                icon: const Icon(Icons.person_add, size: 19),
                label: const Text("Register", style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        selectedColor: widget.selectedColor,
        unSelectedColor: widget.unSelectedColor,
        currentPageIndex: 3,
        routes: ['/', '/discover', '/map', '/authenticate', '/profile'],
        context: context,
      ),
    );
  }
}
