import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'api_interface.dart';
import 'utils.dart';

class Posts extends StatefulWidget {
  const Posts({super.key, required this.title});

  final String title;

  @override
  State<Posts> createState() => _PostsState();
}

class _PostsState extends State<Posts> with SingleTickerProviderStateMixin {
  String? businessType;
  bool loadingRestaurantPosts = true;
  bool loadingFoodBankPosts = true;
  List<dynamic> restaurantPosts = [];
  List<dynamic> foodBankPosts = [];
  final foodController = TextEditingController();
  final quantityController = TextEditingController();
  final locationController = TextEditingController();
  late TabController _tabController;
  DateTime? selectedDate;

  @override
  void initState() {
    _tabController = TabController(vsync: this, length: 2);
    super.initState();
  }

  @override
  void dispose() {
    _tabController.dispose();
    foodController.dispose();
    quantityController.dispose();
    locationController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
        context: context,
        initialDate: selectedDate ?? DateTime.now(),
        firstDate: DateTime.now(),
        lastDate: DateTime(2101));
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
      });
    }
  }

  void getRestaurantData() async {
    loadingRestaurantPosts = true;

    List<dynamic> postsData = (await API().getRestaurantPosts()).data;

    for (final post in postsData) {
      post["time"] = DateTime.parse(post["time"]);
      post["exp"] = DateTime.parse(post["exp"]);
    }

    setState(() {
      restaurantPosts = postsData;
      loadingRestaurantPosts = false;
    });
  }

  void getFoodBankData() async {
    loadingFoodBankPosts = true;

    List<dynamic> postsData = (await API().getFoodBankPosts()).data;

    setState(() {
      foodBankPosts = postsData;
      loadingFoodBankPosts = false;
    });
  }

  Widget _foodBankPostBuilder(BuildContext context, int index) {
    return Card(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Column(
            children: [
              Text(
                foodBankPosts[index]['title'],
                style: const TextStyle(fontSize: 20),
                textAlign: TextAlign.center,
              ),
              Text(
                foodBankPosts[index]['location'],
                style: const TextStyle(fontSize: 15),
              ),
              Text(
                foodBankPosts[index]['description'],
                style: const TextStyle(fontSize: 15),
              ),
            ],
          ),
        ),
      ),
    );
  }

  List<TableRow> _restaurantPostBuilder() {
    List<TableRow> rows = <TableRow>[];
    for (Map<String, dynamic> post in restaurantPosts) {
      rows.add(
        TableRow(children: [
          Center(child: Text(post['food'])),
          Center(child: Text(post['quantity'].toString())),
          Center(child: Text(DateFormat.yMd().format(post['exp']))),
        ]),
      );
    }

    return rows;
  }

  void createRestaurantPost() {
    API()
        .createRestaurantPost(
          food: foodController.text,
          quantity: int.parse(quantityController.text),
          location: locationController.text,
          expiration: (selectedDate!.millisecondsSinceEpoch ~/ 1000),
        )
        .then((value) => setState(() {
              foodController.text = '';
              quantityController.text = '';
              locationController.text = '';
              selectedDate = null;
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('The post was created successfully.'),
                ),
              );
            }))
        .onError(
      (error, stackTrace) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('There was an error when creating the post.'),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    API().verify().then((value) {
      if (value is Map) {
        if (value.containsKey('error')) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(value["error"]),
            ),
          );
        } else {
          setState(() {});
        }
      }

      if (API().loggedIn() && businessType == null) {
        API().getAccountType().then((businessResponse) {
          setState(() {
            businessType = businessResponse?.toLowerCase();
          });
        });
      }
    });

    if (loadingRestaurantPosts) {
      getRestaurantData();
    }

    if (loadingFoodBankPosts) {
      getFoodBankData();
    }

    return Scaffold(
      appBar: appbarComponent(
        title: widget.title,
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(
              icon: Icon(Icons.restaurant),
              text: 'Restaurant Posts',
            ),
            Tab(
              icon: Icon(Icons.food_bank),
              text: 'Food Bank Posts',
            ),
          ],
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(5, 0, 5, 0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: [
                    Center(
                      child: SingleChildScrollView(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            API().loggedIn()
                                ? businessType == 'restaurant'
                                    ? Column(
                                        children: [
                                          Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.center,
                                            crossAxisAlignment:
                                                CrossAxisAlignment.center,
                                            children: [
                                              Expanded(
                                                child: buildTextField(
                                                  labelText: "Food",
                                                  controller: foodController,
                                                  dense: true,
                                                  icon: Icons.fastfood,
                                                  context: context,
                                                  border: false,
                                                ),
                                              ),
                                              const SizedBox(width: 2),
                                              Expanded(
                                                child: buildTextField(
                                                  labelText: "Quantity (Lbs)",
                                                  controller:
                                                      quantityController,
                                                  dense: true,
                                                  icon: Icons.numbers,
                                                  context: context,
                                                  border: false,
                                                ),
                                              ),
                                            ],
                                          ),
                                          buildTextField(
                                            labelText: "Location",
                                            controller: locationController,
                                            dense: true,
                                            icon: Icons.location_pin,
                                            context: context,
                                            border: false,
                                          ),
                                          TextButton.icon(
                                            icon: const Icon(
                                                Icons.calendar_today),
                                            label: Text(selectedDate == null
                                                ? 'Select Expiration Date'
                                                : 'Expiration Date: ${DateFormat.yMd().format(selectedDate!)}'),
                                            onPressed: () =>
                                                _selectDate(context),
                                          ),
                                          ElevatedButton.icon(
                                            onPressed: selectedDate == null
                                                ? null
                                                : createRestaurantPost,
                                            icon: const Icon(Icons.new_label),
                                            label: const Text("Create Post"),
                                          ),
                                        ],
                                      )
                                    : const Text(
                                        'Please login a restaurant account to post.')
                                : const Text(
                                    'Please login with a restaurant account to post.'),
                            const SizedBox(height: 20),
                            loadingRestaurantPosts
                                ? const CircularProgressIndicator(
                                    color: Color.fromRGBO(100, 125, 155, 1),
                                    strokeWidth: 3,
                                  )
                                : restaurantPosts.isEmpty
                                    ? const Text('No Posts Yet!',
                                        style: TextStyle(fontSize: 16))
                                    : Table(
                                        children: const [
                                              TableRow(
                                                children: [
                                                  Center(
                                                    child: Text(
                                                      'Food',
                                                      style: TextStyle(
                                                          fontSize: 17),
                                                    ),
                                                  ),
                                                  Center(
                                                    child: Text(
                                                      'Quantity',
                                                      style: TextStyle(
                                                          fontSize: 17),
                                                    ),
                                                  ),
                                                  Center(
                                                    child: Text(
                                                      'Expiration',
                                                      style: TextStyle(
                                                          fontSize: 17),
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ] +
                                            _restaurantPostBuilder(),
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
                            ElevatedButton.icon(
                              onPressed: () {
                                if (businessType == 'restaurant') {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text(
                                        'Please use a food bank account to create food bank posts.',
                                      ),
                                    ),
                                  );
                                } else {
                                  context.go('/create-foodbank-post');
                                }
                              },
                              icon: const Icon(Icons.new_label),
                              label: const Text('Create A Food Bank Post'),
                            ),
                            loadingFoodBankPosts
                                ? const CircularProgressIndicator(
                                    color: Color.fromRGBO(100, 125, 155, 1),
                                    strokeWidth: 3,
                                  )
                                : foodBankPosts.isEmpty
                                    ? const Text('No Posts Yet! Add One!',
                                        style: TextStyle(fontSize: 16))
                                    : ListView.builder(
                                      physics: const NeverScrollableScrollPhysics(),
                                      shrinkWrap: true,
                                      padding: const EdgeInsets.all(5.5),
                                      itemCount: foodBankPosts.length,
                                      itemBuilder: _foodBankPostBuilder,
                                    ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              TextButton.icon(
                onPressed: () async {
                  if (context.mounted) context.go('/charts');
                },
                icon: const Icon(Icons.trending_up, size: 19),
                label: const Text(
                  "View Posting Trends",
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: 2,
        context: context,
      ),
    );
  }
}
