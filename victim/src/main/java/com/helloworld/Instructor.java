package com.helloworld;

import lombok.*;
import javax.persistence.*;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Entity
@Table(name = "instructors")
public class Instructor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "instructor_name")
    private String instructorName;

    @Column(name = "employee_id")
    private String employeeId;

    @Column(name = "email")
    private String email;

    @Column(name = "office_location")
    private String officeLocation;
}
