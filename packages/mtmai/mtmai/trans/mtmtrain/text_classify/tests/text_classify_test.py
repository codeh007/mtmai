import unittest



# 测试数据
test_texts = [
    "Scientists discover a new planet in our solar system, challenging existing astronomical theories.",
    "The stock market experiences a significant drop in value, causing concerns among investors.",
    "Apple announces the launch of a new MacBook Pro with enhanced performance and features.",
    "Breaking news: Political unrest in the capital city as protests escalate in response to government actions.",
    "Microsoft releases a major update for Windows 10, introducing new functionalities and improvements.",
    "Researchers find a potential cure for a common disease, marking a significant breakthrough in medical science.",
    "Tesla unveils its latest electric car model, promising longer battery life and advanced autonomous driving capabilities.",
    "International summit discusses climate change solutions, bringing together leaders from around the world.",
    "Google introduces a new feature in its search engine to provide more accurate and personalized results.",
    "Economic indicators point to a recovery in the job market, with increasing employment opportunities.",
    "SpaceX successfully launches a satellite into orbit, expanding global communication capabilities.",
    "Tech company invests in renewable energy research to promote sustainable and eco-friendly solutions.",
    "New study reveals the impact of social media on mental health, raising awareness about online well-being.",
    "Facebook announces stricter policies for content moderation to address issues related to misinformation and harmful content.",
    "Global health organization issues a warning about a new virus outbreak, urging precautionary measures.",
    "Amazon expands its drone delivery program to new regions, aiming to improve the efficiency of package delivery.",
    "Government introduces regulations to address cybersecurity threats, safeguarding national digital infrastructure.",
    "Automaker recalls vehicles due to safety concerns, prioritizing consumer safety and satisfaction.",
    "Artificial intelligence breakthrough in medical diagnostics shows promising results for early disease detection.",
    "Virtual reality technology used in innovative educational programs to enhance learning experiences for students.",
]

# 科技类别的测试文本
tech_test_texts = [
    "Apple's latest iPhone features cutting-edge technology and a sleek design.",
    "SpaceX announces plans for a mission to Mars, revolutionizing space exploration.",
    "Google develops a new artificial intelligence algorithm for image recognition.",
    "Microsoft unveils a breakthrough in quantum computing, paving the way for advanced computational capabilities.",
    "Tesla introduces a self-driving electric car with advanced safety features.",
    "Researchers create a new material with potential applications in renewable energy technology.",
    "Amazon launches a state-of-the-art data center for cloud computing services.",
    "Virtual reality startup raises significant funding for the development of immersive gaming experiences.",
    "Artificial intelligence company achieves a major milestone in natural language processing.",
    "NASA collaborates with private tech companies to develop next-generation space technologies.",
    "Tech giant invests in the development of a high-speed, low-latency 5G network.",
    "Blockchain technology gains widespread adoption in the finance and healthcare sectors.",
    "Electric vehicle startup introduces a groundbreaking energy-efficient charging system.",
    "Robotics company unveils a humanoid robot with advanced capabilities for various industries.",
    "Drones equipped with AI are used for innovative applications in agriculture and environmental monitoring.",
    "Augmented reality devices become increasingly popular for educational and entertainment purposes.",
    "Biotechnology firm pioneers gene-editing techniques for potential medical breakthroughs.",
    "Cybersecurity company develops an advanced threat detection system to protect against cyber attacks.",
    "Renewable energy startup achieves a major milestone in the development of efficient solar panels.",
    "Innovative tech solutions contribute to the advancement of smart cities around the world.",
]

# 食品类别的测试文本
food_test_texts = [
    "New restaurant opens with a menu featuring diverse and delicious cuisines.",
    "Cooking show introduces a unique recipe for a popular dessert.",
    "Food festival showcases a variety of local and international dishes.",
    "Health benefits of a balanced diet are discussed in a nutrition seminar.",
    "Celebrity chef launches a new line of gourmet products.",
    "Vegan and gluten-free options available at a trendy new cafe.",
    "Street food vendors offer tasty and affordable snacks in the city center.",
    "Review of a new cookbook with innovative and easy-to-follow recipes.",
    "Traditional recipes passed down through generations shared in a culinary blog.",
    "Food enthusiasts gather for a community potluck with homemade dishes.",
    "Exploration of exotic ingredients and flavors in a travel and food documentary.",
    "Tips for sustainable and eco-friendly food choices in a lifestyle magazine.",
    "Cooking competition features skilled chefs showcasing their culinary expertise.",
    "Local farmers market promotes fresh and locally sourced produce.",
    "Artisanal chocolate brand recognized for its quality and ethical sourcing.",
    "Interactive cooking class teaches participants how to prepare a gourmet meal.",
    "Food and wine pairing event highlights the perfect combinations for a memorable dining experience.",
    "Review of a popular street food vendor known for its signature dishes.",
    "Exploration of unique street food offerings in different cities around the world.",
    "New technology in food production aims to address global challenges and enhance sustainability.",
]

class TestClasssify(unittest.TestCase):
    def test_hello_world(self):
        # result = hello_world()
        # self.assertEqual(result, "Hello, World!")
        print ("hello")




if __name__ == '__main__':
    unittest.main()
