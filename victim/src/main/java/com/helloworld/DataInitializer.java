kpackage com.helloworld;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final InstructorRepository instructorRepository;
    private final StudentRepository studentRepository;
    private final CourseRepository courseRepository;
    private final DepartmentRepository departmentRepository;

    public DataInitializer(
            InstructorRepository instructorRepository,
            StudentRepository studentRepository,
            CourseRepository courseRepository,
            DepartmentRepository departmentRepository
    ) {
        this.instructorRepository = instructorRepository;
        this.studentRepository = studentRepository;
        this.courseRepository = courseRepository;
        this.departmentRepository = departmentRepository;
    }

    @Override
    public void run(String... args) {

        String[][] departments = {
                {"Informatics Faculty", "Building A", "if@vu.lt", "Dr. James Harrington"},
                {"Mathematics Faculty", "Building B", "mf@vu.lt", "Prof. Laura Bennett"},
                {"Physics Faculty", "Building C", "phys@vu.lt", "Dr. Michael Carter"},
                {"Engineering Faculty", "Building D", "eng@vu.lt", "Prof. Hannah Mitchell"}
        };

        for (String[] d : departments) {
            Department dep = new Department();
            dep.setDepartmentName(d[0]);
            dep.setBuilding(d[1]);
            dep.setEmail(d[2]);
            dep.setHeadOfDepartment(d[3]);
            departmentRepository.save(dep);
        }

        String[][] instructors = {
                {"Dr. James Harrington", "EMP1001", "jaha4721@vu.lt", "Building A"},
                {"Prof. Emma Thompson", "EMP1002", "emth6631@vu.lt", "Building A"},
                {"Dr. Andrew Foster", "EMP1003", "anfo7750@vu.lt", "Building A"},
                {"Prof. Isabella Gray", "EMP1004", "isgr7713@vu.lt", "Building A"},
                {"Prof. Laura Bennett", "EMP2001", "labe1938@vu.lt", "Building B"},
                {"Dr. Matthew Hughes", "EMP2002", "math9951@vu.lt", "Building B"},
                {"Prof. Sophie Grant", "EMP2003", "sogr3384@vu.lt", "Building B"},
                {"Dr. William Stone", "EMP2004", "wist5829@vu.lt", "Building B"},
                {"Dr. Michael Carter", "EMP3001", "mica5821@vu.lt", "Building C"},
                {"Prof. Sarah Collins", "EMP3002", "saco7402@vu.lt", "Building C"},
                {"Dr. Thomas Reed", "EMP3003", "thre1205@vu.lt", "Building C"},
                {"Prof. Victoria Hayes", "EMP3004", "viha6640@vu.lt", "Building C"},
                {"Prof. Hannah Mitchell", "EMP4001", "hami4487@vu.lt", "Building D"},
                {"Dr. David Reynolds", "EMP4002", "dare9183@vu.lt", "Building D"},
                {"Prof. Olivia Parker", "EMP4003", "olpa3901@vu.lt", "Building D"},
                {"Dr. Richard Lawson", "EMP4004", "rila1029@vu.lt", "Building D"}
        };

        for (String[] i : instructors) {
            Instructor ins = new Instructor();
            ins.setInstructorName(i[0]);
            ins.setEmployeeId(i[1]);
            ins.setEmail(i[2]);
            ins.setOfficeLocation(i[3]);
            instructorRepository.save(ins);
        }

        String[][] courses = {
                {"Intro to Programming", "Dr. James Harrington", "jaha4721@vu.lt"},
                {"Web Development", "Prof. Emma Thompson", "emth6631@vu.lt"},
                {"Software Engineering", "Dr. Andrew Foster", "anfo7750@vu.lt"},
                {"Advanced Java", "Prof. Isabella Gray", "isgr7713@vu.lt"},
                {"Discrete Mathematics", "Prof. Laura Bennett", "labe1938@vu.lt"},
                {"Statistics", "Dr. Matthew Hughes", "math9951@vu.lt"},
                {"Linear Algebra", "Prof. Sophie Grant", "sogr3384@vu.lt"},
                {"Probability Theory", "Dr. William Stone", "wist5829@vu.lt"},
                {"Physics I", "Dr. Michael Carter", "mica5821@vu.lt"},
                {"Quantum Mechanics", "Prof. Sarah Collins", "saco7402@vu.lt"},
                {"Thermodynamics", "Dr. Thomas Reed", "thre1205@vu.lt"},
                {"Electromagnetism", "Prof. Victoria Hayes", "viha6640@vu.lt"},
                {"Computer Networks", "Prof. Hannah Mitchell", "hami4487@vu.lt"},
                {"Operating Systems", "Dr. David Reynolds", "dare9183@vu.lt"},
                {"Cloud Computing", "Prof. Olivia Parker", "olpa3901@vu.lt"},
                {"Cyber Security", "Dr. Richard Lawson", "rila1029@vu.lt"}
        };

        for (String[] c : courses) {
            Course co = new Course();
            co.setCourseName(c[0]);
            co.setInstructor(c[1]);
            co.setEmail(c[2]);
            courseRepository.save(co);
        }

        String[][] students = {
                {"Alex", "Turner", "S1001", "Computer Science"},
                {"Sophie", "Walker", "S1002", "Engineering"},
                {"Ethan", "Phillips", "S1003", "Mathematics"},
                {"Mia", "Roberts", "S1004", "Physics"},
                {"Noah", "Edwards", "S1005", "Computer Science"},
                {"Ava", "Campbell", "S1006", "Engineering"},
                {"Liam", "Parker", "S1007", "Mathematics"},
                {"Isla", "Evans", "S1008", "Physics"},
                {"Oliver", "Murphy", "S1009", "Computer Science"},
                {"Amelia", "Baker", "S1010", "Engineering"},
                {"James", "Cooper", "S1011", "Mathematics"},
                {"Emily", "Richardson", "S1012", "Physics"},
                {"Benjamin", "Cox", "S1013", "Computer Science"},
                {"Charlotte", "Howard", "S1014", "Engineering"},
                {"Lucas", "Ward", "S1015", "Mathematics"},
                {"Grace", "Brooks", "S1016", "Physics"},
                {"Henry", "Kelly", "S1017", "Computer Science"},
                {"Zoe", "Bailey", "S1018", "Engineering"},
                {"Daniel", "Wood", "S1019", "Mathematics"},
                {"Lily", "Barnes", "S1020", "Physics"}
        };

        for (String[] s : students) {
            Student st = new Student();
            st.setFirstName(s[0]);
            st.setLastName(s[1]);
            st.setStudentId(s[2]);
            st.setMajor(s[3]);
            studentRepository.save(st);
        }
    }
}
