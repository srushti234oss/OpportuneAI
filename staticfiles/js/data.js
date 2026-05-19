// ═══════════════════════════════════════════════
// OpportuneAI — DATA FILE
// Replace fetch() calls here when Django is ready
// ═══════════════════════════════════════════════

const OPPORTUNITIES = [
  // ─── SCHOLARSHIPS ───
  { id:1, title:"AICTE National Scholarship", org:"AICTE", type:"scholarship",
    icon:"🎓", iconBg:"#ede9fe", desc:"The AICTE scholarship supports meritorious engineering students across India. Covers tuition fees and provides a monthly maintenance allowance. Available for all branches.",
    deadline:"2025-07-30", minGpa:8.0, stipend:"₹25,000/year", location:"All India",
    requiredSkills:["Academic Excellence"], eligibleYears:[1,2,3,4], tags:["Merit","Govt"] },

  { id:2, title:"Buddy4Study Merit Scholarship", org:"Buddy4Study Foundation", type:"scholarship",
    icon:"🏆", iconBg:"#fef3c7", desc:"Annual merit scholarship open to students from all disciplines. Apply once, be considered for multiple scholarships. Supports education and skill development.",
    deadline:"2025-08-31", minGpa:7.0, stipend:"₹10,000–₹50,000", location:"All India",
    requiredSkills:["Academic Excellence"], eligibleYears:[1,2,3,4], tags:["Merit","NGO"] },

  { id:3, title:"NSP Central Sector Scholarship", org:"National Scholarship Portal", type:"scholarship",
    icon:"📜", iconBg:"#d1fae5", desc:"Government scholarship for class XII passed students pursuing higher education. Income-based eligibility. One of India's largest scholarship programs.",
    deadline:"2025-09-15", minGpa:6.0, stipend:"₹12,000/year", location:"All India",
    requiredSkills:["Academic Excellence"], eligibleYears:[1,2], tags:["Govt","Income-based"] },

  { id:4, title:"INSPIRE Scholarship – DST", org:"Dept. of Science & Technology", type:"scholarship",
    icon:"🌟", iconBg:"#dbeafe", desc:"Scholarship for the top 1% students in Class XII board exams pursuing Natural and Basic Sciences at B.Sc./B.S./Int. M.S. level.",
    deadline:"2025-07-10", minGpa:9.0, stipend:"₹80,000/year", location:"All India",
    requiredSkills:["Academic Excellence","Physics","Mathematics"], eligibleYears:[1,2], tags:["Science","Govt","Top 1%"] },

  // ─── INTERNSHIPS ───
  { id:5, title:"Google PM Fellowship", org:"Google India", type:"internship",
    icon:"🟦", iconBg:"#dbeafe", desc:"12-week immersive program for students passionate about product management. Work directly with Google PMs on live products. Includes mentorship and pre-placement offer opportunity.",
    deadline:"2025-07-15", minGpa:7.5, stipend:"₹80,000/month", location:"Bengaluru",
    requiredSkills:["Python","Data Analysis","SQL","Communication","Product Thinking"], eligibleYears:[3,4], tags:["PM","MNC","PPO"] },

  { id:6, title:"Microsoft SWE Internship", org:"Microsoft India", type:"internship",
    icon:"🪟", iconBg:"#dbeafe", desc:"Join Microsoft as a Software Engineering intern. Work on real Azure, Microsoft 365, or Xbox products. Strong PPO conversion rate. Open to all CS/IT branches.",
    deadline:"2025-09-01", minGpa:7.0, stipend:"₹1,00,000/month", location:"Hyderabad / Noida",
    requiredSkills:["Data Structures","Algorithms","C++","Java","System Design"], eligibleYears:[3,4], tags:["SWE","MNC","PPO"] },

  { id:7, title:"Amazon ML Internship", org:"Amazon India", type:"internship",
    icon:"📦", iconBg:"#fef3c7", desc:"Build and scale machine learning systems at Amazon across product recommendations, supply chain optimisation, fraud detection, and Alexa NLU.",
    deadline:"2025-08-10", minGpa:7.5, stipend:"₹1,20,000/month", location:"Bengaluru / Hyderabad",
    requiredSkills:["Machine Learning","Python","Data Structures","Deep Learning","SQL"], eligibleYears:[3,4], tags:["ML","AI","MNC","PPO"] },

  { id:8, title:"ISRO Research Internship", org:"ISRO", type:"internship",
    icon:"🚀", iconBg:"#d1fae5", desc:"Work with ISRO scientists on cutting-edge space technology. Projects span satellite communication, remote sensing, propulsion, and data analysis from space missions.",
    deadline:"2025-07-10", minGpa:8.5, stipend:"₹15,000/month", location:"Bengaluru / Trivandrum",
    requiredSkills:["Python","MATLAB","Physics","Data Analysis","Linux"], eligibleYears:[3,4], tags:["Research","Space","Govt"] },

  { id:9, title:"Goldman Sachs Quant Internship", org:"Goldman Sachs", type:"internship",
    icon:"💹", iconBg:"#dbeafe", desc:"Work with GS quant researchers on financial modelling, risk analysis, and algorithmic trading systems. 10-week intensive with strong PPO.",
    deadline:"2025-10-01", minGpa:8.0, stipend:"₹1,50,000/month", location:"Bengaluru / Mumbai",
    requiredSkills:["Python","Statistics","Mathematics","Machine Learning","SQL"], eligibleYears:[3,4], tags:["Finance","Quant","MNC"] },

  { id:10, title:"Infosys InStep Global Internship", org:"Infosys", type:"internship",
    icon:"🌐", iconBg:"#ede9fe", desc:"Join Infosys globally at offices in USA, Europe, or Australia. Work on AI, digital transformation, and enterprise tech projects.",
    deadline:"2025-09-15", minGpa:7.5, stipend:"International stipend", location:"USA / Europe",
    requiredSkills:["Java","SQL","Communication","Problem Solving","Agile"], eligibleYears:[3,4], tags:["Global","MNC","International"] },

  // ─── HACKATHONS ───
  { id:11, title:"Smart India Hackathon 2025", org:"Ministry of Education", type:"hackathon",
    icon:"🇮🇳", iconBg:"#fef3c7", desc:"India's biggest hackathon — solve real problems for government ministries and PSUs. Teams of 6 students. Multiple problem statements across agriculture, healthcare, education, fintech.",
    deadline:"2025-08-01", minGpa:0, stipend:"₹1,00,000 prize", location:"Multiple cities",
    requiredSkills:["Problem Solving","Web Development","Machine Learning","Team Collaboration"], eligibleYears:[1,2,3,4], tags:["Team","Govt","Prize"] },

  { id:12, title:"Flipkart GRiD Engineering Challenge", org:"Flipkart", type:"hackathon",
    icon:"🛍️", iconBg:"#fef3c7", desc:"Engineering challenge where students solve real e-commerce problems. Top teams get fast-track interview slots and internship offers at Flipkart.",
    deadline:"2025-07-25", minGpa:0, stipend:"Cash prizes + PPO", location:"Online + Bengaluru finale",
    requiredSkills:["Web Development","Machine Learning","Problem Solving","Team Collaboration"], eligibleYears:[1,2,3,4], tags:["E-commerce","PPO"] },

  { id:13, title:"HackWithInfy 2025", org:"Infosys", type:"hackathon",
    icon:"💡", iconBg:"#ede9fe", desc:"Infosys's annual national hackathon for engineering students. Solve real business problems with technology. Winners get direct placement interviews at Infosys.",
    deadline:"2025-09-10", minGpa:6.0, stipend:"₹75,000 + placement", location:"Online",
    requiredSkills:["Problem Solving","JavaScript","Python","API Development"], eligibleYears:[2,3,4], tags:["Placement","National"] },

  // ─── FELLOWSHIPS ───
  { id:14, title:"Tata Trusts Rural Tech Fellowship", org:"Tata Trusts", type:"fellowship",
    icon:"🌱", iconBg:"#d1fae5", desc:"6-month fellowship for students passionate about using technology for social good. Work in rural communities on digital literacy, agri-tech, and financial inclusion.",
    deadline:"2025-08-20", minGpa:6.5, stipend:"₹20,000/month + accommodation", location:"Rural Maharashtra / Bihar",
    requiredSkills:["Communication","Web Development","Problem Solving","Community Development"], eligibleYears:[2,3,4], tags:["Social Impact","Rural"] },

  { id:15, title:"INSA Summer Research Fellowship", org:"Indian National Science Academy", type:"fellowship",
    icon:"🔬", iconBg:"#ede9fe", desc:"8-week summer research fellowship working alongside India's top scientists. Projects in physics, chemistry, biology, and interdisciplinary fields. Travel allowance and hostel provided.",
    deadline:"2025-06-15", minGpa:8.5, stipend:"₹10,000/month + accommodation", location:"New Delhi",
    requiredSkills:["Research","Academic Excellence","Scientific Writing","Physics"], eligibleYears:[2,3], tags:["Research","Science","Govt"] },

  { id:16, title:"iSPIRT Product Fellowship", org:"iSPIRT Foundation", type:"fellowship",
    icon:"📱", iconBg:"#dbeafe", desc:"India's premier product management fellowship. Learn from founders and PMs who built India Stack, UPI, and Aadhaar. 3-month intensive, fully remote.",
    deadline:"2025-07-31", minGpa:0, stipend:"Unpaid · High value network", location:"Remote",
    requiredSkills:["Product Thinking","Communication","Data Analysis","Problem Solving"], eligibleYears:[2,3,4], tags:["Product","Startup","Network"] },
];

// ─── SKILL + INTEREST OPTIONS ───
const SKILL_OPTIONS = [
  "Python","Java","C++","JavaScript","SQL","MATLAB","R",
  "Machine Learning","Deep Learning","Data Analysis","Data Structures",
  "Algorithms","Web Development","System Design","Linux","Cloud",
  "Statistics","Mathematics","Physics","Communication",
  "Team Collaboration","Problem Solving","Research","Product Thinking",
  "Agile","Scientific Writing","Academic Excellence","Community Development",
  "API Development","React","Django","TensorFlow"
];

const INTEREST_OPTIONS = [
  "Artificial Intelligence","Web Development","Finance & Fintech",
  "Space & Astronomy","Social Impact","Research","Product Management",
  "Data Science","Cybersecurity","Sustainability","Healthcare",
  "Agriculture","Education","Gaming","Robotics","Open Source"
];

// ─── COURSES TO CLOSE SKILL GAPS ───
const SKILL_COURSES = {
  "Python": { platform: "NPTEL", link: "https://nptel.ac.in", name: "Python for Data Science" },
  "Machine Learning": { platform: "Coursera", link: "https://coursera.org", name: "ML Specialisation (Andrew Ng)" },
  "Deep Learning": { platform: "fast.ai", link: "https://fast.ai", name: "Practical Deep Learning" },
  "Data Structures": { platform: "YouTube", link: "#", name: "DSA by Striver" },
  "Algorithms": { platform: "LeetCode", link: "https://leetcode.com", name: "Blind 75 Problems" },
  "SQL": { platform: "SQLZoo", link: "https://sqlzoo.net", name: "SQL Interactive Tutorial" },
  "System Design": { platform: "YouTube", link: "#", name: "System Design Primer" },
  "Statistics": { platform: "Khan Academy", link: "https://khanacademy.org", name: "Statistics & Probability" },
  "Mathematics": { platform: "NPTEL", link: "https://nptel.ac.in", name: "Engineering Mathematics" },
  "Communication": { platform: "Coursera", link: "https://coursera.org", name: "Business Communication" },
  "Web Development": { platform: "The Odin Project", link: "https://theodinproject.com", name: "Full Stack Web Dev" },
  "Product Thinking": { platform: "PM School", link: "https://pmschool.io", name: "Product Management 101" },
  "Research": { platform: "Coursera", link: "https://coursera.org", name: "Research Methods" },
  "Scientific Writing": { platform: "Coursera", link: "https://coursera.org", name: "Science Writing & Communication" },
};