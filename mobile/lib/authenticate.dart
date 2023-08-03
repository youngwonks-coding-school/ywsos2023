import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:go_router/go_router.dart';
import 'api_interface.dart';
import 'utils.dart';

class Authenticate extends StatefulWidget {
  const Authenticate({super.key, required this.title});

  final String title;

  @override
  State<Authenticate> createState() => _AuthenticateState();
}

class _AuthenticateState extends State<Authenticate> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final emailRegex = RegExp(
      r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,253}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,253}[a-zA-Z0-9])?)*$");
  final List<bool> _accountType = <bool>[true, false];

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();

    super.dispose();
  }

  void login() async {
    Response? response =
        await API().login(emailController.text, passwordController.text);
    if (context.mounted) {
      if (response == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
                'The server was unable to be reached! Please try again later.'),
          ),
        );
      } else if (response.statusCode! < 400) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Successfully logged in!'),
          ),
        );
        context.go('/');
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Your email or password is incorrect!'),
          ),
        );
      }
    }
  }

  void register() async {
    Response? response = await API().register(
        emailController.text, passwordController.text, _accountType[0]);
    if (context.mounted) {
      if (response == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
                'The server was unable to be reached! Please try again later.'),
          ),
        );
      } else if (response.statusCode! < 400) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Successfully registered!'),
          ),
        );
        context.go('/');
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('An account with that email already exists!'),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appbarComponent(title: widget.title),
      resizeToAvoidBottomInset: true,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: DefaultTabController(
            length: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                const TabBar(
                  tabs: [
                    Tab(text: "Login"),
                    Tab(text: "Register"),
                  ],
                ),
                Expanded(
                  child: TabBarView(
                    children: [
                      Center(
                        child: SingleChildScrollView(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              buildTextField(
                                labelText: "Email",
                                controller: emailController,
                                icon: Icons.email,
                                context: context,
                                validate: (String? text) {
                                  if (!emailRegex.hasMatch(text!)) {
                                    return "Please enter a valid email address!";
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 5),
                              buildTextField(
                                labelText: "Password",
                                controller: passwordController,
                                obscureText: true,
                                icon: Icons.lock,
                                context: context,
                                validate: (String? text) {
                                  if (text!.length < 8) {
                                    return "Please enter a password with at least 8 characters!";
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 6),
                              ElevatedButton.icon(
                                onPressed: login,
                                icon: const Icon(Icons.login, size: 19),
                                label: const Text("Login",
                                    style: TextStyle(fontSize: 16)),
                              ),
                            ],
                          ),
                        ),
                      ),
                      Center(
                        child: SingleChildScrollView(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              buildTextField(
                                labelText: "Email",
                                controller: emailController,
                                icon: Icons.email,
                                context: context,
                                validate: (String? text) {
                                  if (!emailRegex.hasMatch(text!)) {
                                    return "Please enter a valid email address!";
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 5),
                              buildTextField(
                                labelText: "Password",
                                controller: passwordController,
                                obscureText: true,
                                icon: Icons.lock,
                                context: context,
                                validate: (String? text) {
                                  if (text!.length < 8) {
                                    return "Please enter a password with at least 8 characters!";
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 6),
                              ToggleButtons(
                                direction: Axis.horizontal,
                                onPressed: (int index) {
                                  setState(() {
                                    for (int i = 0;
                                        i < _accountType.length;
                                        i++) {
                                      _accountType[i] = i == index;
                                    }
                                  });
                                },
                                borderRadius:
                                    const BorderRadius.all(Radius.circular(8)),
                                selectedBorderColor: Colors.transparent,
                                selectedColor: Colors.white,
                                fillColor:
                                    const Color.fromRGBO(180, 160, 130, 1),
                                color: Colors.red[800],
                                constraints: const BoxConstraints(
                                  minHeight: 40.0,
                                  minWidth: 80.0,
                                ),
                                isSelected: _accountType,
                                children: const [
                                  Padding(
                                    padding: EdgeInsets.all(8),
                                    child: Row(
                                      children: [
                                        Icon(
                                          Icons.restaurant_rounded,
                                          size: 20,
                                        ),
                                        Text('Restaurant'),
                                      ],
                                    ),
                                  ),
                                  Padding(
                                    padding: EdgeInsets.symmetric(
                                        vertical: 0, horizontal: 8),
                                    child: Row(
                                      children: [
                                        Icon(
                                          Icons.food_bank_rounded,
                                          size: 34,
                                        ),
                                        Text('Food Bank'),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                              ElevatedButton.icon(
                                onPressed: register,
                                icon: const Icon(Icons.person_add, size: 19),
                                label: const Text("Register",
                                    style: TextStyle(fontSize: 16)),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: 3,
        context: context,
      ),
    );
  }
}
